#!/usr/bin/env python
DESC="""EPP script to calculate amount in ng from concentration and volume 
udf:s in Clarity LIMS. The script calculates the concentration in nM from
ng/ul.

Johannes Alneberg, Science for Life Laboratory, Stockholm, Sweden
Adapted by Rikard Erlandsson, Clinical Genomics . . .
""" 
from argparse import ArgumentParser

from genologics.lims import Lims
from genologics.config import BASEURI,USERNAME,PASSWORD

from genologics.entities import Process
from genologics.epp import EppLogger

import logging
import sys

def apply_calculations(lims,artifacts,udf1,udf2,result_udf,epp_logger, f):
    logging.info(("result_udf: {0}, udf_conc: {1}, "
                  "udf_size: {2}").format(result_udf,udf1,udf2))

    for artifact in artifacts:
        try:
            artifact.udf[result_udf]
        except KeyError:
            artifact.udf[result_udf]=0

        logging.info(("Updating: Artifact id: {0}, "
                     "result_udf: {1}, udf_conc: {2}, "
                     "udf_size: {3}").format(artifact.id, 
                            artifact.udf[result_udf],
                            artifact.udf[udf1],
                            artifact.udf[udf2]))
							
        factor = 1e6 / (328.3 * 2 * artifact.udf[udf2])
        artifact.udf[result_udf] = artifact.udf[udf1] * factor
        artifact.put()
        logging.info('Updated {0} to {1}.'.format(result_udf,
                                                 artifact.udf[result_udf]))

        f.write(("Calculating: Artifact[{5}] id:{0}, "
                     "  {3} (ng/ul)   {4} (bp) "
                     "           {1}  =  {2} nM").format(artifact.id,
							artifact.samples[0].id,
                            artifact.udf[result_udf],
                            artifact.udf[udf1],
                            artifact.udf[udf2],
                            artifact.samples[0].name))
            
def check_udf_is_defined(artifacts, udf):
    """ Filter and Warn if udf is not defined for any of artifacts. """
    filtered_artifacts = []
    incorrect_artifacts = []
    for artifact in artifacts:
        if (udf in artifact.udf):
            filtered_artifacts.append(artifact)
        else:
            logging.warning(("Found artifact for sample {0} with {1} "
                             "undefined/blank, skipping").format(artifact.samples[0].name, udf))
            incorrect_artifacts.append(artifact)
    return filtered_artifacts, incorrect_artifacts


def check_udf_has_value(artifacts, udf, value):
    """ Filter artifacts on undefined udf or if udf has wrong value. """
    filtered_artifacts = []
    incorrect_artifacts = []
    for artifact in artifacts:
        if udf in artifact.udf and (artifact.udf[udf] == value):
            filtered_artifacts.append(artifact)
        elif udf in artifact.udf:
            incorrect_artifacts.append(artifact)
            logging.warning(("Filtered out artifact for sample: {0}"
                          ", due to wrong {1}").format(artifact.samples[0].name, udf))
        else:
            incorrect_artifacts.append(artifact)
            logging.warning(("Filtered out artifact for sample: {0}"
                          ", due to undefined/blank {1}").format(artifact.samples[0].name, udf))

    return filtered_artifacts, incorrect_artifacts

def main(lims,args,epp_logger):
    p = Process(lims,id = args.pid)
    udf_factor1 = 'Concentration (ng/ul)'
    result_udf = 'Concentration (nM)'
    udf_factor2 = 'Size (bp)'

    if args.aggregate:
        artifacts = p.all_inputs(unique=True)
    else:
        all_artifacts = p.all_outputs(unique=True)
        artifacts = filter(lambda a: a.output_type == "Analyte", all_artifacts)

#    print rrtifacts
    correct_artifacts, wrong_factor1 = check_udf_is_defined(artifacts, udf_factor1)
    correct_artifacts, wrong_factor2 = check_udf_is_defined(correct_artifacts, udf_factor2)

    f = open(args.res, "a")

    if correct_artifacts:
        apply_calculations(lims, correct_artifacts, udf_factor1,
                           udf_factor2, result_udf, epp_logger, f)
    
    f.close()


    d = {'ca': len(correct_artifacts),
         'ia': len(wrong_factor1)+ len(wrong_factor2) }

    abstract = ("Updated {ca} artifact(s), skipped {ia} artifact(s) with "
                "wrong and/or blank values for some udfs.").format(**d)

    print >> sys.stderr, abstract # stderr will be logged and printed in GUI


if __name__ == "__main__":
    # Initialize parser with standard arguments and description
    parser = ArgumentParser(description=DESC)
    parser.add_argument('--pid',
                        help='Lims id for current Process')
    parser.add_argument('--log',
                        help='Log file for runtime info and errors.')
    parser.add_argument('--aggregate', action='store_true',
                        help=('Use this tag if current Process is an '
                              'aggregate QC step'))
    parser.add_argument('--res',
                        help='Results file.')
    args = parser.parse_args()

    lims = Lims(BASEURI, USERNAME, PASSWORD)
    lims.check_version()

    with EppLogger(args.log, lims=lims, prepend=True) as epp_logger:
        main(lims, args, epp_logger)
