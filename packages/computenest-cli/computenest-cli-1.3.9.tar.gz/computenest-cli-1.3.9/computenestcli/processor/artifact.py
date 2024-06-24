import time
import json
import os
import re
from Tea.exceptions import TeaException
from computenestcli.common.decorator import retry_on_exception
from computenestcli.service.artifact import ArtifactService
from computenestcli.service.file import FileService
from computenestcli.service.credentials import CredentialsService
from computenestcli.common.util import Util
from computenestcli.processor.image import ImageProcessor
from computenestcli.common import constant
from computenestcli.common.context import Context

TRUE = 'True'
FALSE = 'False'
UPDATE_ARTIFACT = 'UpdateArtifact'
AVAILABLE = 'Available'
DELIVERING = 'Delivering'
DATA = 'data'
RESULT = 'result'
IMAGE_BUILDER = 'ImageBuilder'
ACR_IMAGE_BUILDER = 'AcrImageBuilder'
HELM_CHART_BUILDER = 'HelmChartBuilder'
ARTIFACT = 'artifact'
DRAFT = 'draft'
REGION_ID = 'regionId'
COMMAND_CONTENT = 'CommandContent'
ENTITY_ALREADY_EXIST_DRAFT_ARTIFACT = 'EntityAlreadyExist.DraftArtifact'
ARTIFACT_VERSION_NOT_FOUND = 'EntityNotExist.ArtifactVersion'
ARTIFACT_STATUS_NOT_SUPPORT_OPERATION = 'OperationDenied'


class ArtifactProcessor:

    def __init__(self, context):
        self.context = context

    def _get_file_artifact_url(self, artifact_name):
        get_artifact_data = json.loads(ArtifactService.get_artifact(self.context, artifact_name).body.artifact_property)
        url = get_artifact_data.get(constant.URL)
        return url

    def _create_image_from_image_builder(self, data, artifact_data):
        data_image = data.get(IMAGE_BUILDER)
        id_image = artifact_data.get(constant.ARTIFACT_PROPERTY).get(constant.IMAGE_ID)
        id_image_match = Util.regular_expression(id_image)
        data_image_oos = data_image.get(id_image_match[1])
        region_id = data_image_oos[constant.REGION_ID]
        command_content = data_image_oos[COMMAND_CONTENT]
        # 识别命令语句中的占位符
        pattern = r'\$\{Artifact\.(.*?)\.ArtifactProperty\.Url\}'
        matches = re.findall(pattern, command_content)
        if matches:
            artifact_key = matches[0].strip()
            artifact_name = data[constant.ARTIFACT].get(artifact_key, {}).get(constant.ARTIFACT_NAME)
            url = self._get_file_artifact_url(artifact_name)
            parts = url.split("/")
            # 截取文件部署物下载链接的后半部分
            artifact_url = parts[-2] + "/" + parts[-1]
            placeholder = f'${{Artifact.{artifact_key}.ArtifactProperty.Url}}'
            # 替换真正的url
            command_content = command_content.replace(placeholder, artifact_url)
            data_image_oos[COMMAND_CONTENT] = command_content
        data_image_oos = Util.lowercase_first_letter(data_image_oos)
        region_id_image = data_image_oos[REGION_ID]
        image_context = Context(region_id_image, self.context.credentials)
        image_processor = ImageProcessor(image_context)
        return region_id, image_processor.process_image(data_image_oos)

    def _create_acrimage_from_acrimage_builder(self, data, artifact_data, file_path_config):
        artifact_type = artifact_data.get(constant.ARTIFACT_TYPE)
        image = ImageProcessor(self.context)
        data_acr_image = data.get(ACR_IMAGE_BUILDER)
        acr_image = artifact_data.get(constant.ARTIFACT_PROPERTY).get(constant.REPO_NAME)
        acr_image_match = Util.regular_expression(acr_image)
        data_acr_image = data_acr_image.get(acr_image_match[1])
        file_path = os.path.join(os.path.dirname(file_path_config), data_acr_image[constant.DOCKER_FILE_PATH])
        acr_image_name = data_acr_image[constant.REPO_NAME]
        acr_image_tag = data_acr_image[constant.TAG]
        # 如果DockerfilePath存在，运行Dockerfile并打标推送
        if data_acr_image[constant.DOCKER_FILE_PATH]:
            image.process_acr_image(acr_image_name, acr_image_tag, file_path)
            repo_id = self._get_repo_id(artifact_type, acr_image_name)
        # 若不存在认为线上仓库已存在相关容器镜像
        else:
            repo_id = self._get_repo_id(artifact_type, acr_image_name)
            # 查到repo_id后检索所有已存在的tag，检查提供的tag是否存在
            tags = ArtifactService.list_acr_image_tags(self.context, repo_id, artifact_type).body.images
            tag_values = []
            for item in tags:
                tag_value = item.tag
                tag_values.append(tag_value)
            if acr_image_tag in tag_values:
                acr_image_tag = acr_image_tag
            else:
                raise ValueError("Provided acr image tag does not exist")
        return acr_image_name, repo_id, acr_image_tag

    def _get_repo_id(self, artifact_type, acr_image_name):
        response_body = ArtifactService.list_acr_image_repositories(self.context, artifact_type, acr_image_name).body
        if response_body and response_body.repositories:
            return response_body.repositories[0].repo_id
        else:
            raise Exception("No Repo found")

    def _create_helmchart_from_helmchart_builder(self, data, artifact_data, file_path_config):
        artifact_type = artifact_data.get(constant.ARTIFACT_TYPE)
        image = ImageProcessor(self.context)
        helm_chart_data = data.get(HELM_CHART_BUILDER)
        helm_chart = artifact_data.get(constant.ARTIFACT_PROPERTY).get(constant.REPO_NAME)
        helm_chart_match = Util.regular_expression(helm_chart)
        data_helm_chart = helm_chart_data.get(helm_chart_match[1])
        file_path = os.path.join(os.path.dirname(file_path_config), data_helm_chart[constant.HELM_CHART_PATH])
        helm_chart_name = data_helm_chart[constant.REPO_NAME]
        helm_chart_tag = data_helm_chart[constant.TAG]

        if data_helm_chart[constant.HELM_CHART_PATH]:
            image.process_helm_chart(file_path)
            helm_chart_repo_id = self._get_repo_id(artifact_type, helm_chart_name)
        # 若不存在认为线上仓库已存在相关容器镜像
        else:
            helm_chart_repo_id = self._get_repo_id(artifact_type, helm_chart_name)
        # 查到repo_id后检索所有已存在的tag，检查提供的tag是否存在
        tags = ArtifactService.list_acr_image_tags(self.context, helm_chart_repo_id, artifact_type).body.images
        tag_values = []
        for item in tags:
            tag_value = item.tag
            tag_values.append(tag_value)
        if helm_chart_tag in tag_values:
            helm_chart_tag = helm_chart_tag
        else:
            raise ValueError("Invalid or non-existent Helm chart version provided.")

        return helm_chart_name, helm_chart_repo_id, helm_chart_tag

    def _replace_artifact_file_path_with_url(self, file_path):
        data = CredentialsService.get_artifact_repository_credentials(self.context, constant.FILE)
        file_artifact_url = FileService.put_file(data, file_path, ARTIFACT)
        return file_artifact_url

    def _release_artifact(self, artifact_id, artifact_name):
        ArtifactService.release_artifact(self.context, artifact_id)
        while True:
            # 定时检测部署物发布状态
            try:
                data_response = ArtifactService.get_artifact(self.context, artifact_name, 'draft')
                artifact_status = data_response.body.status
                if artifact_status == DELIVERING:
                    print('The artifact is being released...')
            except TeaException as e:
                if e.code == ARTIFACT_VERSION_NOT_FOUND:
                    print('The release is complete')
                    break
                else:
                    raise
            time.sleep(25)

    def get_artifact_detail(self, artifact_id, data_yaml, artifact_key):
        response = ArtifactService.get_artifact(self.context, '', '', artifact_id)
        artifact_type = response.body.artifact_type
        artifact_name = response.body.name
        description = response.body.description
        support_region_ids = response.body.support_region_ids
        artifact_property = json.loads(response.body.artifact_property)
        parameters = {
            constant.ARTIFACT_TYPE: artifact_type,
            constant.ARTIFACT_NAME: artifact_name,
            constant.DESCRIPTION: description,
            constant.ARTIFACT_PROPERTY: artifact_property,
            constant.SUPPORT_REGION_IDS: support_region_ids
        }
        data_yaml[constant.ARTIFACT][artifact_key] = parameters
        return data_yaml

    @Util.measure_time
    def process(self, data_config, file_path_config, update_artifact='', version_name=''):
        data_artifact = data_config.get(constant.ARTIFACT)
        for artifact_data in data_artifact.values():
            if constant.ARTIFACT_NAME in artifact_data:
                artifact_type = artifact_data.get(constant.ARTIFACT_TYPE)
                artifact_name = artifact_data.get(constant.ARTIFACT_NAME)
                if version_name:
                    artifact_data[constant.VERSION_NAME] = version_name
                if update_artifact == TRUE:
                    artifact_data[UPDATE_ARTIFACT] = True
                else:
                    artifact_data[UPDATE_ARTIFACT] = False
                artifact_data_list = ArtifactService.list_artifact(self.context, artifact_name)
                if len(artifact_data_list.body.artifacts) == 0:
                    if artifact_type == constant.FILE:
                        # 将相对路径替换成绝对路径
                        file_path = os.path.join(os.path.dirname(file_path_config),
                                                 artifact_data.get(constant.ARTIFACT_PROPERTY).get(constant.URL))
                        # 将文件部署物的本地路径替换成Url
                        artifact_data[constant.ARTIFACT_PROPERTY][
                            constant.URL] = self._replace_artifact_file_path_with_url(file_path)
                    elif artifact_type == constant.ECS_IMAGE:
                        if IMAGE_BUILDER in data_config:
                            # 利用oos模版创建镜像
                            region_id, image_id = self._create_image_from_image_builder(data_config, artifact_data)
                            artifact_data[constant.ARTIFACT_PROPERTY][constant.REGION_ID] = region_id
                            artifact_data[constant.ARTIFACT_PROPERTY][constant.IMAGE_ID] = image_id
                    elif artifact_type == constant.ACR_IMAGE:
                        acr_image_name, repo_id, acr_image_tag = self._create_acrimage_from_acrimage_builder(
                            data_config, artifact_data, file_path_config)
                        artifact_data[constant.ARTIFACT_PROPERTY][constant.REPO_NAME] = acr_image_name
                        artifact_data[constant.ARTIFACT_PROPERTY][constant.TAG] = acr_image_tag
                        artifact_data[constant.ARTIFACT_PROPERTY][constant.REPO_ID] = repo_id
                    elif artifact_type == constant.HELM_CHART:
                        helm_chart_name, helm_chart_id, helm_chart_tag = self._create_helmchart_from_helmchart_builder(
                            data_config, artifact_data, file_path_config)
                        artifact_data[constant.ARTIFACT_PROPERTY][constant.REPO_NAME] = helm_chart_name
                        artifact_data[constant.ARTIFACT_PROPERTY][constant.TAG] = helm_chart_tag
                        artifact_data[constant.ARTIFACT_PROPERTY][constant.REPO_ID] = helm_chart_id
                    data_create_artifact = ArtifactService.create_artifact(self.context, artifact_data)
                    artifact_id = data_create_artifact.body.artifact_id
                    current_time = Util.get_current_time()
                    print("===========================")
                    print("Successfully created a new artifact!")
                    print("The artifact name: ", artifact_name)
                    print("The artifact id: ", artifact_id)
                    print("Completion time: ", current_time)
                    print("===========================")
                    self._release_artifact(artifact_id, artifact_name)
                elif not artifact_data.get(UPDATE_ARTIFACT):
                    artifact_id = artifact_data_list.body.artifacts[0].artifact_id
                    current_time = Util.get_current_time()
                    print("===========================")
                    print("No need to update the artifact")
                    print("The artifact name: ", artifact_name)
                    print("The artifact id: ", artifact_id)
                    print("Completion time: ", current_time)
                    print("===========================")
                else:
                    if artifact_type == constant.FILE:
                        file_url_existed = self._get_file_artifact_url(artifact_name)
                        # 将相对路径替换成绝对路径
                        file_path = os.path.join(os.path.dirname(file_path_config),
                                                 artifact_data.get(constant.ARTIFACT_PROPERTY).get(constant.URL))
                        result_artifact = FileService.check_file_repeat(file_url_existed, file_path)
                        # 检查文件部署物是否重复，重复则不再上传，使用现有Url
                        if result_artifact:
                            artifact_data[constant.ARTIFACT_PROPERTY][constant.URL] = file_url_existed.split('?')[0]
                        else:
                            artifact_data[constant.ARTIFACT_PROPERTY][
                                constant.URL] = self._replace_artifact_file_path_with_url(file_path)
                    elif artifact_type == constant.ECS_IMAGE:
                        if IMAGE_BUILDER in data_config:
                            # 利用oos模版创建镜像
                            region_id, image_id = self._create_image_from_image_builder(data_config, artifact_data)
                            artifact_data[constant.ARTIFACT_PROPERTY][constant.REGION_ID] = region_id
                            artifact_data[constant.ARTIFACT_PROPERTY][constant.IMAGE_ID] = image_id
                    elif artifact_type == constant.ACR_IMAGE:
                        acr_image_name, repo_id, acr_image_tag = self._create_acrimage_from_acrimage_builder(
                            data_config, artifact_data, file_path_config)
                        artifact_data[constant.ARTIFACT_PROPERTY][constant.REPO_NAME] = acr_image_name
                        artifact_data[constant.ARTIFACT_PROPERTY][constant.TAG] = acr_image_tag
                        artifact_data[constant.ARTIFACT_PROPERTY][constant.REPO_ID] = repo_id
                    elif artifact_type == constant.HELM_CHART:
                        helm_chart_name, helm_chart_id, helm_chart_tag = self._create_helmchart_from_helmchart_builder(
                            data_config, artifact_data, file_path_config)
                        artifact_data[constant.ARTIFACT_PROPERTY][constant.REPO_NAME] = helm_chart_name
                        artifact_data[constant.ARTIFACT_PROPERTY][constant.TAG] = helm_chart_tag
                        artifact_data[constant.ARTIFACT_PROPERTY][constant.REPO_ID] = helm_chart_id
                    artifact_id = artifact_data_list.body.artifacts[0].artifact_id
                    self._create_or_update_artifact(artifact_data, artifact_id)
                    current_time = Util.get_current_time()
                    print("===========================")
                    print("Successfully updated the artifact!")
                    print("The artifact name: ", artifact_name)
                    print("The artifact id: ", artifact_id)
                    print("Completion time: ", current_time)
                    print("===========================")
                    self._release_artifact(artifact_id, artifact_name)
                data_response = ArtifactService.list_artifact(self.context, artifact_name)
                max_version = int(data_response.body.artifacts[0].max_version)
                if artifact_data.get(constant.ARTIFACT_PROPERTY).get(constant.VERSION):
                    version = artifact_data.get(constant.ARTIFACT_PROPERTY).get(constant.VERSION)
                    if version == 'back':
                        artifact_version = max_version - 1
                    elif int(version) <= max_version:
                        artifact_version = artifact_data.get(constant.ARTIFACT_PROPERTY).get(constant.VERSION)
                    else:
                        raise ValueError("Wrong version")
                else:
                    artifact_version = max_version
                artifact_data[constant.ARTIFACT_ID] = artifact_id
                artifact_data[constant.ARTIFACT_VERSION] = artifact_version
        return data_artifact

    @retry_on_exception(max_retries=10, delay=2, backoff=2, exceptions=(TeaException,))
    def _create_or_update_artifact(self, artifact_data, artifact_id):
        try:
            ArtifactService.create_artifact(self.context, artifact_data, artifact_id)
        except TeaException as e:
            if e.code == ENTITY_ALREADY_EXIST_DRAFT_ARTIFACT:
                try:
                    ArtifactService.update_artifact(self.context, artifact_data, artifact_id)
                except TeaException as e:
                    if e.code == ARTIFACT_STATUS_NOT_SUPPORT_OPERATION:
                        raise
            else:
                raise
