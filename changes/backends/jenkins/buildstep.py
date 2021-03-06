from __future__ import absolute_import

from datetime import datetime, timedelta
from flask import current_app

from changes.backends.base import UnrecoverableException
from changes.buildsteps.base import BuildStep

from .builder import JenkinsBuilder
from .factory_builder import JenkinsFactoryBuilder
from .generic_builder import JenkinsGenericBuilder


class JenkinsBuildStep(BuildStep):
    def __init__(self, job_name=None):
        self.job_name = job_name

    def get_builder(self, app=current_app):
        return JenkinsBuilder(app=app, job_name=self.job_name)

    def get_label(self):
        return 'Execute job "{0}" on Jenkins'.format(self.job_name)

    def execute(self, job):
        builder = self.get_builder()
        builder.create_job(job)

    def update(self, job):
        builder = self.get_builder()
        builder.sync_job(job)

    def update_step(self, step):
        builder = self.get_builder()
        try:
            builder.sync_step(step)
        except UnrecoverableException:
            # bail if the step has been pending for too long as its likely
            # Jenkins fell over
            if step.date_created < datetime.utcnow() - timedelta(minutes=5):
                return
            raise

    def cancel(self, job):
        builder = self.get_builder()
        builder.cancel_job(job)

    def fetch_artifact(self, step, artifact):
        builder = self.get_builder()
        builder.sync_artifact(step, artifact)


class JenkinsFactoryBuildStep(JenkinsBuildStep):
    def __init__(self, job_name=None, downstream_job_names=()):
        self.job_name = job_name
        self.downstream_job_names = downstream_job_names

    def get_builder(self, app=current_app):
        return JenkinsFactoryBuilder(
            app=app,
            job_name=self.job_name,
            downstream_job_names=self.downstream_job_names,
        )


class JenkinsGenericBuildStep(JenkinsBuildStep):
    def __init__(self, job_name, script, cluster, path=''):
        self.job_name = job_name
        self.script = script
        self.cluster = cluster
        self.path = path

    def get_builder(self, app=current_app):
        return JenkinsGenericBuilder(
            app=app,
            job_name=self.job_name,
            script=self.script,
            cluster=self.cluster,
            path=self.path,
        )
