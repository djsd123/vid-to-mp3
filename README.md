# vid-to-mp3
Teeny-Tiny Streamlit app to grab the audio from streaming video


[Docker]: https://www.docker.com/
[pulumi]: https://www.pulumi.com/docs/get-started/install/
[Python]: https://www.python.org/downloads/

Deploys a [Docker] image to an AWS ECR repository


## Requirements

| Name     | Version             |
|----------|---------------------|
| [Pulumi] | > = 3.55.0, < 4.0.0 |
| [Python] | = 3.10.x            |
| [Docker] | (Docker Desktop)    |


## Providers

| Name   | Version            |
|--------|--------------------|
| aws    | > = 5.0.0, < 6.0.0 |
| awsx   | > = 1.0.2, < 2.0.0 |
| pulumi | > = 3.0.0, < 4.0.0 |



## Usage

__Deploy to AWS__

Set required environment variables

```shell
export AWS_REGION=<AWS_REGION>
export PULUMI_BACKEND_URL=s3://<YOUR-BUCKET>
```

Install Requirements

```shell
pip install -r requirements.txt
```

Create Stack

```shell
pulumi stack init
```

Plan/Preview

```shell
pulumi preview
```

Deploy

```shell
pulumi up
```

Cleanup

```shell
pulumi destroy -y
```


__Run Locally__

Within `src` directory

```shell
cd src
```

Build [Docker] image

```shell
docker image build -t vid-to-mp3 .
```

Run [Docker] container

```shell
docker container run -t -p 8501:8501 vid-to-mp3
```

You should now see the app running in your browser at [localhost:8501](http://localhost:8501)
