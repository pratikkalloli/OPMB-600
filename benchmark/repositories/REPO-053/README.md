# FirmwareFleet

FirmwareFleet is a synthetic firmware release and rollout registry. Release manifests bind a device family, semantic version, image digest, and minimum bootloader. Devices only install signed releases newer than their active version. The baseline uses RSA-PSS; the reference uses ML-DSA-65.

Install requirements.txt and run pytest from this directory.
