#!/usr/bin/env python

import logging
import optparse
import subprocess
import sys
import os


def main():
        usage = "Usage: %prog -i <input_file> [options]"
        parser = optparse.OptionParser(usage=usage)

        parser.add_option(
                "-d", "--docker",
                action="store_true",
                dest="build_docker_opt",
                default=False,
                help="Build docker container"
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
                default="WARNING",
                help="Set logging level: CRITICAL, ERROR, WARNING, INFO,\
                DEBUG (default: WARNING)"
                )
        options, args = parser.parse_args()

        ######################################################################
        # Logging

        numeric_level = getattr(logging, options.loglevel.upper(), None)
        print numeric_level
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

        if not (options.build_docker_opt or options.build_packages_opt):
            parser.error('Must specify a file to modify \"-d\" and a line number \"-l\"')
        else:
            prepare_build()


def run(command, allow_failure=False, shell=False):
    """Run shell command (convenience wrapper around subprocess).
       Need to import subprocess
       Need to import sys
    """
    out = None
    logging.debug("{}".format(command))
    try:
        if shell:
            out = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=shell)
        else:
            out = subprocess.check_output(command.split(), stderr=subprocess.STDOUT)
        out = out.decode('utf-8').strip()
        # logging.debug("Command output: {}".format(out))
    except subprocess.CalledProcessError as e:
        if allow_failure:
            logging.warn("Command '{}' failed with error: {}".format(command, e.output))
            return None
        else:
            logging.error("Command '{}' failed with error: {}".format(command, e.output))
            sys.exit(1)
    except OSError as e:
        if allow_failure:
            logging.warn("Command '{}' failed with error: {}".format(command, e))
            return out
        else:
            logging.error("Command '{}' failed with error: {}".format(command, e))
            sys.exit(1)
    else:
        return out


def prepare_build():
    branch = "stable"
    if not os.path.exists("build_output"):
        logging.debug('Creating build_output dir')
        os.makedirs("build_output", mode=0755)
    PWD = os.path.dirname(os.path.realpath(__file__))
    docker_builder_cmdlder_cmd = "docker run --rm -ti -v " \
     + PWD + "/build_script:/build_script --name influxdb_build docker.io/schabrolles/ubuntu_ppc64le:16.04 /build_script/build_influxdb.sh " + branch
    run(docker_builder_cmdlder_cmd, allow_failure=False, shell=False)


if __name__ == "__main__":
        main()
