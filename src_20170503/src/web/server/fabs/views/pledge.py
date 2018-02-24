# -*- coding: utf-8 -*- 
from flask import Blueprint, request, json, abort, current_app, jsonify
from ..services import  PledgeService
from ..base import helpers
from . import route
from werkzeug import secure_filename
import os
PledgeService = PledgeService()

bp = Blueprint('pledge', __name__, url_prefix='/pledge')

@route(bp, '/PaperContract', methods=['POST'])
def PaperContract():
    return  PledgeService.PaperContract(**request.json)

@route(bp,'/upload',methods=['POST'])
def upload():
    files = request.files.getlist('file')
    file = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = os.path.join(upload_path,secure_filename(file.filename))
    file.save(local_path)
    gty_id = request.form.get('gty_id')
    return PledgeService.upload(local_path,gty_id)

@route(bp, '/othersave', methods=['POST'])
def othersave_Pledge():
    PledgeService.save(**request.json)
    return True

@route(bp, '/otherupdate', methods=['POST'])
def otherupdate_Pledge():
    PledgeService.update(**request.json)
    return True

@route(bp,'/deleteGTY',methods=['GET'])
def delete_gty():
    return PledgeService.delete(**request.args)

@route(bp,'/query',methods=['GET'])
def query_gty():
    return PledgeService.query(**request.args)

@route(bp, '/perstubsave', methods=['POST'])
def perstubsave_Pledge():
    PledgeService.save(**request.json)
    return True

@route(bp, '/perstubupdate', methods=['POST'])
def perstubupdate_Pledge():
    PledgeService.update(**request.json)
    return True

@route(bp, '/stubsave', methods=['POST'])
def stubsave_Pledge():
    PledgeService.save(**request.json)
    return True

@route(bp, '/stubupdate', methods=['POST'])
def stubupdate_Pledge():
    PledgeService.update(**request.json)
    return True

@route(bp, '/savingsave', methods=['POST'])
def savingsave_Pledge():
    PledgeService.save(**request.json)
    return True

@route(bp, '/savingupdate', methods=['POST'])
def savingupdate_Pledge():
    PledgeService.update(**request.json)
    return True

@route(bp, '/ndsave', methods=['POST'])
def ndsave_Pledge():
    PledgeService.save(**request.json)
    return True

@route(bp, '/ndupdate', methods=['POST'])
def ndupdate_Pledge():
    PledgeService.update(**request.json)
    return True

@route(bp, '/inssave', methods=['POST'])
def inssave_Pledge():
    PledgeService.save(**request.json)
    return True

@route(bp, '/insupdate', methods=['POST'])
def insupdate_Pledge():
    PledgeService.update(**request.json)
    return True

@route(bp, '/crdsave', methods=['POST'])
def crdsave_Pledge():
    PledgeService.save(**request.json)
    return True

@route(bp, '/crdupdate', methods=['POST'])
def crdupdate_Pledge():
    PledgeService.update(**request.json)
    return True

@route(bp, '/fe_savingsave', methods=['POST'])
def fe_savingsave_Pledge():
    PledgeService.save(**request.json)
    return True

@route(bp, '/fe_savingupdate', methods=['POST'])
def fe_savingupdate_Pledge():
    PledgeService.update(**request.json)
    return True

@route(bp, '/ware_lstsave', methods=['POST'])
def ware_lstsave_Pledge():
    PledgeService.save(**request.json)
    return True

@route(bp, '/ware_lstupdate', methods=['POST'])
def ware_lstupdate_Pledge():
    PledgeService.update(**request.json)
    return True

@route(bp, '/dosave', methods=['POST'])
def dosave_Pledge():
    PledgeService.save(**request.json)
    return True

@route(bp, '/doupdate', methods=['POST'])
def doupdate_Pledge():
    PledgeService.update(**request.json)
    return True

@route(bp, '/vchsave', methods=['POST'])
def vchsave_Pledge():
    PledgeService.save(**request.json)
    return True

@route(bp, '/vchupdate', methods=['POST'])
def vchupdate_Pledge():
    PledgeService.update(**request.json)
    return True

@route(bp, '/vch_qlfsave', methods=['POST'])
def vch_qlfsave_Pledge():
    PledgeService.save(**request.json)
    return True

@route(bp, '/vch_qlfupdate', methods=['POST'])
def vch_qlfupdate_Pledge():
    PledgeService.update(**request.json)
    return True

@route(bp, '/bondsave', methods=['POST'])
def bondsave_Pledge():
    PledgeService.save(**request.json)
    return True

@route(bp, '/bondupdate', methods=['POST'])
def bondupdate_Pledge():
    PledgeService.update(**request.json)
    return True

@route(bp, '/ipo_intsave', methods=['POST'])
def ipo_intsave_Pledge():
    PledgeService.save(**request.json)
    return True

@route(bp, '/ipo_intupdate', methods=['POST'])
def ipo_intupdate_Pledge():
    PledgeService.update(**request.json)
    return True

@route(bp, '/non_ipo_intsave', methods=['POST'])
def non_ipo_intsave_Pledge():
    PledgeService.save(**request.json)
    return True

@route(bp, '/non_ipo_intupdate', methods=['POST'])
def non_ipo_intupdate_Pledge():
    PledgeService.update(**request.json)
    return True

@route(bp, '/acc_recsave', methods=['POST'])
def acc_recsave_Pledge():
    PledgeService.save(**request.json)
    return True

@route(bp, '/acc_recupdate', methods=['POST'])
def acc_recupdate_Pledge():
    PledgeService.update(**request.json)
    return True

@route(bp, '/cvrgsave', methods=['POST'])
def cvrgsave_Pledge():
    PledgeService.save(**request.json)
    return True

@route(bp, '/cvrgupdate', methods=['POST'])
def cvrgupdate_Pledge():
    PledgeService.update(**request.json)
    return True

@route(bp, '/accpsave', methods=['POST'])
def accpsave_Pledge():
    PledgeService.save(**request.json)
    return True

@route(bp, '/accpupdate', methods=['POST'])
def accpupdate_Pledge():
    PledgeService.update(**request.json)
    return True

@route(bp, '/billsave', methods=['POST'])
def billsave_Pledge():
    PledgeService.save(**request.json)
    return True

@route(bp, '/billupdate', methods=['POST'])
def billupdate_Pledge():
    PledgeService.update(**request.json)
    return True

'''
抵押
'''
@route(bp, '/MrgeBuildingSave', methods=['POST'])
def MrgeBuildingSave():
    PledgeService.save(**request.json)
    return True
@route(bp, '/MrgeEqpSave', methods=['POST'])
def MrgeEqpSave():
    PledgeService.save(**request.json)
    return True
@route(bp, '/MrgeLandSave', methods=['POST'])
def MrgeLandSave():
    PledgeService.save(**request.json)
    return True
@route(bp, '/MrgeOtherSave', methods=['POST'])
def MrgeOtherSave():
    PledgeService.save(**request.json)
    return True
@route(bp, '/MrgeVchSave', methods=['POST'])
def MrgeVchSave():
    PledgeService.save(**request.json)
    return True
@route(bp, '/MrgeMovableSave', methods=['POST'])
def MrgeMovableSave():
    PledgeService.save(**request.json)
    return True
@route(bp, '/MrgeEqpMovableSave', methods=['POST'])
def MrgeEqpMovableSave():
    PledgeService.save(**request.json)
    return True
@route(bp, '/MrgeBuildingUpdate', methods=['POST'])
def MrgeBuildingUpdate():
    PledgeService.update(**request.json)
    return True
@route(bp, '/MrgeLandUpdate', methods=['POST'])
def MrgeLandUpdate():
    PledgeService.update(**request.json)
    return True
@route(bp, '/MrgeVchUpdate', methods=['POST'])
def MrgeVchUpdate():
    PledgeService.update(**request.json)
    return True
@route(bp, '/MrgeEqpUpdate', methods=['POST'])
def MrgeEqpUpdate():
    PledgeService.update(**request.json)
    return True
@route(bp, '/MrgeOtherUpdate', methods=['POST'])
def MrgeOtherUpdate():
    PledgeService.update(**request.json)
    return True

