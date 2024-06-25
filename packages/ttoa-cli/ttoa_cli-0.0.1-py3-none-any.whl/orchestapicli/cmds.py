'''The Orchest API CLI commands.

'''
from orchestapicli.core import Orchest
from tqdm import tqdm
import json
import sys
import typing as t


class OrchestAPICmds:
    def __init__(self, **kwargs):
        url = kwargs.get('url')
        username = kwargs.get('username')
        password = kwargs.get('password')

        self.Orchest = None
        if url:
            self.Orchest = Orchest(url, username, password)

        return
    
    def export_to_json(self, data: t.Any, file_name: str) -> None:
        '''
        Write the data to a JSON file
        '''
        file_name = f'{file_name}.json'
        
        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)

    def get_projects(
        self,
        export: bool,
        **kwargs,
    ) -> list:
        '''Get all projects'''
        projects = self.Orchest.get_projects()

        if export:
            self.export_to_json(projects, sys._getframe().f_code.co_name)
        
        return projects
    
    def get_pipeline_runs(
        self,
        export: bool,
        statusses: list,
        cancel: bool,
        **kwargs,
    ) -> list:
        '''Get all projects'''
        # only started and pending jobs can be cancelled
        if cancel:
            statusses = ['STARTED', 'PENDING']

        pipeline_runs = self.Orchest.get_pipeline_runs(statusses=statusses)

        failed_cancels = []
        if cancel:
            for pipeline_run in tqdm(pipeline_runs['pipeline_runs'], 'Cancel pipeline runs'):
                pipeline_run_id = pipeline_run['uuid']
                job_id = pipeline_run['job_uuid']

                try:
                    self.Orchest.cancel_pipeline_run(job_id, pipeline_run_id)
                except Exception as e:
                    pipeline_run_error = pipeline_run
                    pipeline_run_error['errors']['cancel_pipeline_run'] = str(e)
                    failed_cancels.append(pipeline_run_error)               

        if export:
            self.export_to_json(pipeline_runs, sys._getframe().f_code.co_name)
        
        if failed_cancels:
            print('Some pipeline runs failed to cancel, see the exported file for details')
            self.export_to_json(failed_cancels, 'cancel_pipeline_run_failures')

        return pipeline_runs, failed_cancels