import os
stage = ""

def get_stage_env():
    github_ref = os.environ.get('GITHUB_REF_NAME')

    if 'prod' in github_ref:
        stage = 'PROD'
    elif 'homolog' in github_ref:
        stage = 'HOMOLOG'
    else:
        stage = 'DEV'

    return stage