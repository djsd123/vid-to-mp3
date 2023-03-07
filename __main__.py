"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import ecr
from pulumi_awsx import ecr as ecrx

config = pulumi.Config()
name = config.get('name')
ecr_image_max_days = config.get_int('ecrImageMaxDays')
ecr_image_max_images = config.get_int('ecrImageMaxImages')

tags = {
    'Name': name,
    'Project': pulumi.get_project(),
    'Stack': pulumi.get_stack(),
}

ecr_repository = ecrx.Repository('ecr-repository',
    name=name,
    force_delete=True,

    encryption_configurations=[ecr.RepositoryEncryptionConfigurationArgs(
        encryption_type='AES256'
    )],

    image_scanning_configuration=ecr.RepositoryImageScanningConfigurationArgs(
        scan_on_push=True,
    ),

    lifecycle_policy=ecrx.LifecyclePolicyArgs(
        rules=[
            ecrx.LifecyclePolicyRuleArgs(
                tag_status=ecrx.LifecycleTagStatus.UNTAGGED,
                description=f'Expire images older than {ecr_image_max_days} days',
                maximum_age_limit=ecr_image_max_days,
            ),
            ecrx.LifecyclePolicyRuleArgs(
                tag_status=ecrx.LifecycleTagStatus.ANY,
                description=f'Limit images in repository to {ecr_image_max_images}',
                maximum_number_of_images=ecr_image_max_images,
            )
        ]
    ),

    image_tag_mutability='MUTABLE',
    tags=tags,
)

image = ecrx.Image('image',
    repository_url=ecr_repository.url,
    path='./src',
)

# Export the uri of the image
pulumi.export('image-uri', image.image_uri)
