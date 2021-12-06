import os
from celery import Celery
from api_models import ML_models
from mongodb import db

CELERY_BROKER = os.environ["CELERY_BROKER"]
CELERY_BACKEND = os.environ["CELERY_BACKEND"]

celery = Celery('tasks', broker=CELERY_BROKER, backend=CELERY_BACKEND)

mlmodels = ML_models()


@celery.task(name='mlmodels')
def task(method=None, **kwargs):
    if method == 'get_possible_model':
        return mlmodels.get_available_model()

    elif method == 'create_model':
        return mlmodels.create_model(**kwargs)

    elif method == 'get_all_models':
        return mlmodels.models

    elif method == 'get_model':
        return mlmodels.get_model(**kwargs)

    elif method == 'update_model':
        return mlmodels.update_model(kwargs)

    elif method == 'delete_model':
        return mlmodels.delete_model(**kwargs)

    elif method == 'fit':
        model_id = kwargs['model_id']
        del kwargs['model_id']
        mlmodels.fit(model_id, **kwargs)
        return 'Model is fitted'

    elif method == 'predict':
        model_id = kwargs['model_id']
        del kwargs['model_id']
        pred = mlmodels.predict(model_id, **kwargs)
        return pred

    elif method == 'predict_proba':
        model_id = kwargs['model_id']
        del kwargs['model_id']
        preds_proba = mlmodels.predict_proba(model_id, **kwargs)
        return preds_proba

    elif method == 'get_scores':
        model_id = kwargs['model_id']
        del kwargs['model_id']
        scores = mlmodels.get_scores(model_id, **kwargs)
        return scores


@celery.task(name='add_row')
def add_row(**kwargs):
    db.insert_one(kwargs)
    return 'Row inserted'


@celery.task(name='delete_row')
def delete_row(model_id):
    db.delete_one({'_id': model_id})
    return 'Row deleted'


@celery.task(name='update_row')
def update_row(id_, **kwargs):
    db.find_one_and_replace({'_id': id_}, kwargs)
    return 'Row updated'


@celery.task(name='get_row')
def get_row(model_id):
    data = db.find({'_id': model_id})
    data = [d for d in data][0]
    try:
        if data['model'] != 'Not fitted':
            data['model'] = "Fitted"
    except Exception:
        return 'Wrong id'
    return data