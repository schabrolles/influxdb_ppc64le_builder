#!/usr/bin/env python
#
# s.chabrolles@fr.ibm.com
##############################################################################

import logging
import optparse
import subprocess
import os
import sys
import tarfile

# GLOBAL VARIABLES definition
HOME = os.path.dirname(os.path.realpath(__file__))
DOCKER_UBUNTU = "docker.io/schabrolles/ubuntu_ppc64le:latest"


def main():
        usage = "Usage: %prog [-d <container_name> | -p]"
        parser = optparse.OptionParser(usage=usage)

        parser.add_option(
                "-d", "--docker",
                dest="docker_container_name",
                help="Build docker container with the following name"
                )
        parser.add_option(
                "-p", "--packages",
                action="store_true",
                dest="build_packages_opt",
                default=False,
                help="Create packages (.deb, .rpm, .tar)"
                )
        parser.add_option(
                "-b", "--branch",
                dest="git_branch",
                default="stable",
                help="Choose the influxdb git branch (version) to compile. \
                 (stable, beta, master, 0.13 ...)"
                )

        debug = optparse.OptionGroup(
                parser,
                "debug",
                "The following options are for debugging"
                )
        parser.add_option_group(debug)

        debug.add_option(
                "--loglevel",
                dest="loglevel",
                default="INFO",
                help="Set logging level: CRITICAL, ERROR, WARNING, INFO,\
                DEBUG (default: INFO)"
                )
        options, args = parser.parse_args()

        ######################################################################
        # Logging

        numeric_level = getattr(logging, options.loglevel.upper(), None)
        if not isinstance(numeric_level, int):
                # raise ValueError('Invalid log level: %s' % options.loglevel)
                logging.error('Invalid log level: %s' % options.loglevel)

        logging.basicConfig(
                # level=logging.INFO,
                level=numeric_level,
                format='%(asctime)s %(levelname)s %(message)s'
                )

        ######################################################################
        # Checking parameters

        if not (options.docker_container_name or options.build_packages_opt):
            parser.error(
                "Must specify a build output type: packages \'-p\'"
                "or docker_image \'-d <docker_image_name>\'"
                )
        else:
            ###################################################################
            ###################################################################
            # BEGINIG OF REAL CODE
            ###################################################################
            prepare_build()

            if options.docker_container_name and options.build_packages_opt:
                build_option = "all"
            elif options.build_packages_opt:
                build_option = "packages"
            else:
                build_option = "static"

            build_influxdb(options.git_branch)
            if options.docker_container_name:
                build_influxdb_container(options.docker_container_name)


def prepare_build():
    """ Preparing environement : installing docker and prepreq
    """
    logging.debug("Entering in prepare_build function")

    logging.debug("chdir to {}".format(HOME))
    os.chdir(HOME)

    if not os.path.exists("build_output"):
        logging.debug('Creating build_output dir')
        os.makedirs("build_output", mode=0755)

    try:
        logging.debug("Testing if docker is available")
        cmd = "docker -v"
        docker_version = subprocess.check_output(
            cmd.split(),
            stderr=subprocess.STDOUT)
        docker_version = docker_version.decode("utf-8".strip())

    except subprocess.CalledProcessError as e:
        logging.error(
            "Command '{}' failed with error: {}".format(cmd, e.output)
            )
        sys.exit(1)
    except OSError as e:
        if e.errno == 2:
            logging.debug("docker binary not found ...")
            logging.info("installing docker")
            p = subprocess.Popen("sudo apt-get install -y docker.io".split())
            p.wait()
        else:
            logging.debug(
                "OSError Command '{}' failed with error: {}".format(cmd, e)
                )
            sys.exit(1)

    logging.info(
        "Pulling latest ubuntu_ppc64le docker image ({})".format(DOCKER_UBUNTU)
        )
    p = subprocess.Popen("docker pull {}".format(DOCKER_UBUNTU).split())
    p.wait()


def build_influxdb(branch):
    """ Compile influxdb
    """
    docker_builder_cmd = "docker run --rm"\
        " -v {}/build_script:/build_script"\
        " -v {}/build_output:/build_output"\
        " --name influxdb_build  {}"\
        " /build_script/build_influxdb.sh {}"\
        .format(HOME, HOME, DOCKER_UBUNTU, branch)

    logging.info("Starting build in transient docker container")
    logging.debug("{}".format(docker_builder_cmd))
    p = subprocess.Popen(docker_builder_cmd.split())
    p.wait()


def build_influxdb_container(container_name):
    """ Create influxdb container from static binary
    """
    logging.debug("Entering in build_influxdb_container function")
    influxdb_static_tar = HOME + "/build_docker/influxdb-static_ppc64le.tar.gz"

    if os.path.isfile(influxdb_static_tar):
        logging.debug("Removing previous influxdb tar file")
        os.remove(influxdb_static_tar)

    logging.debug("chdir to {}/build_output".format(HOME))
    os.chdir(HOME + "/build_output")
    tar = tarfile.open(
        HOME + "/build_docker/influxdb-static_ppc64le.tar.gz", "w:gz"
        )

    logging.info("Creating influxdb_tar with all influxdb bin")
    influxdb_files = [
        "influx", "influxd", "influx_inspect", "influx_stress", "influx_tsm"
        ]
    for filename in influxdb_files:
            tar.add(filename)
    tar.close()

    logging.debug("chdir to {}/build_docker".format(HOME))
    os.chdir(HOME + "/build_docker")

    print ""
    logging.info(
        "Building influxdb docker container : {}".format(container_name)
        )
    print""
    p = subprocess.Popen("docker build -t {} .".format(container_name).split())
    p.wait()


if __name__ == "__main__":
        main()
