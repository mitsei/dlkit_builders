"""Utilies for dealing with amazon web services"""

import boto
import time
from boto.s3.key import Key
from boto.cloudfront import distribution


def get_aws_s3_handle(config_map):
    """Convenience function for getting AWS S3 objects

    Added by cjshaw@mit.edu, Jan 9, 2015
    Added to aws_adapter build by birdland@mit.edu, Jan 25, 2015, and added support for Configuration

    """

    url = 'https://' + config_map['s3_bucket'] + '.s3.amazonaws.com' # https://mitodl-repository.s3.amazonaws.com
    connection = boto.connect_s3(config_map['put_public_key'], config_map['put_private_key'])
    bucket = connection.create_bucket(config_map['s3_bucket'])
    repo = Key(bucket)
    return (repo, url)

def get_signed_url(url, config_map):
    """ Convenience function for getting cloudfront signed URL given a saved URL

    cjshaw, Jan 7, 2015

    Follows:
        http://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-creating-signed-url-canned-policy.html#private-content-creating-signed-url-canned-policy-procedure
        http://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/PrivateContent.html
        http://boto.readthedocs.org/en/latest/ref/cloudfront.html

    """
    current_time = int(time.time())
    expires_in = 300  #seconds
    expires = current_time + expires_in
    s3_bucket = config_map['s3_bucket']

    url = url.replace(s3_bucket + '.s3.amazonaws.com', config_map['cloudfront_distro'])

    connection = boto.connect_cloudfront(config_map['cloudfront_public_key'],
                                         config_map['cloudfront_private_key'])
    odl_distro = connection.get_distribution_info(config_map['cloudfront_distro_id'])

    signed_url = odl_distro.create_signed_url(url,
                                              config_map['cloudfront_keypair_id'],
                                              expire_time=expires,
                                              private_key_file=config_map['cloudfront_private_key_file'])
    return signed_url