# AWS ECS를 이용한 애플리케이션 배포 가이드

Dockerfile에서 AWS ECS(Elastic Container Service)를 사용하여 애플리케이션을 배포하려면 다음 단계를 따르세요:

1. 애플리케이션용 Dockerfile 생성
2. Docker 이미지 빌드 및 Amazon ECR(Elastic Container Registry)에 푸시
3. ECS 작업 정의 생성
4. ECS 클러스터 생성 (아직 없는 경우)
5. 작업을 실행할 ECS 서비스 생성

각 단계에 대한 자세한 설명:

## 1. Dockerfile 생성
애플리케이션의 컨테이너 이미지를 정의하는 유효한 Dockerfile을 준비하세요.

## 2. Docker 이미지 빌드 및 Amazon ECR에 푸시

- ECR 저장소 생성:
```
aws ecr create-repository --repository-name autorag-ecs-repo
```

- ECR 레지스트리에 Docker 인증:
```
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 475776939691.dkr.ecr.us-east-1.amazonaws.com
```

- Docker 이미지 빌드:
```
docker build -t autorag/autorag-ecs .
```

- Docker 실행 (Local Docker):
YOUR_AWS_TARGET_PROFILE 는 바꿔준다.
```
docker run -e AWS_DEFAULT_PROFILE=YOUR_AWS_TARGET_PROFILE autorag-ecs
```


- 이미지 태그 지정:
```
docker tag autorag/autorag-ecs:latest 475776939691.dkr.ecr.us-east-1.amazonaws.com/autorag/autorag-ecs:latest
```

- ECR에 이미지 푸시:
```
docker push 475776939691.dkr.ecr.us-east-1.amazonaws.com/autorag/autorag-ecs:latest
```

## 3. ECS 작업 정의 생성
AWS Management Console이나 AWS CLI를 사용할 수 있습니다. AWS CLI 사용 예:

```json
{
  "family": "autorag-ecs-task",
  "containerDefinitions": [
    {
      "name": "autorag-ecs-container",
      "image": "475776939691.dkr.ecr.us-east-1.amazonaws.com/autorag/autorag-ecs:latest",
      "cpu": 1024,
      "memory": 2048,
      "portMappings": [
        {
          "containerPort": 80,
          "hostPort": 80,
          "protocol": "tcp"
        }
      ],
      "essential": true
    }
  ],
  "requiresCompatibilities": [
    "FARGATE"
  ],
  "networkMode": "awsvpc",
  "cpu": "1024",
  "memory": "2048"
}
```

이 JSON을 `task-definition.json`으로 저장한 후 실행:

```
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

## 4. ECS 클러스터 생성 (필요한 경우)
```
aws ecs create-cluster --cluster-name my-cluster
```

## 5. 작업을 실행할 ECS 서비스 생성
```
aws ecs create-service --cluster my-cluster --service-name autorag-ecs-service --task-definition autorag-ecs-task:1 --desired-count 1 --launch-type FARGATE --network-configuration "awsvpcConfiguration={subnets=[subnet-12345678],securityGroups=[sg-12345678]}"
```

이 명령어는 작업 정의의 인스턴스 하나를 실행하는 서비스를 생성합니다.

주의: 계정ID, 리전, 서브넷 ID, 보안 그룹 ID 등의 플레이스홀더 값을 실제 AWS 계정 정보로 교체하세요.