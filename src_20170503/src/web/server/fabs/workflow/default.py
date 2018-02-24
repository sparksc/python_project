# -*- coding:utf-8 -*-
from ..database import get_session
from ..model.user import User
from ..model.transaction import *
from ..model.application import *
from ..model.approve import *
from ..model.task import *
from ..model.credit import *
from .parameter import *
from .task import get_task
from decimal import Decimal
import logging
from sqlalchemy import distinct, func

def static_assign(task):
    session = get_session(task)
    user_name = get_parameter(task.activity, u'用户')
    task.user = session.query(User).filter(User.user_name==user_name).one()
    logging.debug("session:%s"%str(session))


#lendingproposition_task             贷款申请
#investigate_task                    预审
#subbranch_assessment_task           支行风险评价
#subbranch_review_task               支行审查
#subbranch_deliberation_task         支行审贷小组审议
#subbranch_president_task            支行长审批


def lendingproposition_task(task):
    u"""贷款申请"""
    pass

def chcproposition_task(task):
    u"""转贷大表申请"""
    pass

def investigate_task(task):
    u"""预审"""
    pass

def write_report_task(task):
    u""" 撰写调查报告"""
    pass

def subbranch_assessment_task(task):
    """支行风险评价"""
    pass

def subbranch_review_task(task):
    """支行审查"""
    pass

def subbranch_deliberation_task(task):
    """支行审贷小组审议"""
    # TODO: merge to fabs project !
    '''
    session = get_session(task)
    comment_count = session.query(distinct(ApplicationComment.comment_user_id)).filter(ApplicationComment.transaction_activity_id==task.transaction_activity_id).count()
    # 3人以上流程流转
    if comment_count >= 3:
        task.finish()
    '''
    pass

def subbranch_president_task(task):
    """支行长审议"""
    pass

def discount_investigate_task(task):
    u"""预审"""
    pass

def discount_write_report_task(task):
    u"""贴现撰写调查报告"""
    pass

def discount_subbranch_assessment_task(task):
    """贴现支行风险评价"""
    pass

def discount_subbranch_review_task(task):
    """贴现支行审查"""
    pass

def discount_subbranch_deliberation_task(task):
    """贴现支行审贷小组审议"""
    session = get_session(task)
    logging.debug("#####################")
    logging.debug(task)
    logging.debug("#####################")
    return False

def discount_subbranch_president_task(task):
    """贴现支行长审议"""
    pass

def loan_application_task(task):
    """客户经理进行面签和办理抵质押手续"""
    pass

def subbranch_approve_task(task):
    """支行长审批"""
    pass

def credit_loan_task(task):
    """客户经理放款"""
    pass

def check_ticket_task(task):
    """贴现验票"""
    pass

def discount_approve_task(task):
    """贴现支行长审批"""
    pass

def discount_loan_task(task):
    """贴现放款"""
    pass

def accountant_check_task(task):
    """会计验票"""
    pass

def entering_info_task(task):
    """客户经理录入信息"""
    pass

def invest_application_task(task):
    """投资申请"""
    pass

def invest_review_task(task):
    """投资复核"""
    pass

def invest_term_deliberation_task(task):
    """投资审议小组审议"""
    session = get_session(task)
    logging.debug("#####################")
    logging.debug(task)
    logging.debug("#####################")
    return False
def finance_riskowners_task(task):
    """财务部负责人审查"""
    pass


def capital_riskowners_task(task):
    """资金部负责人审查"""
    pass

def invest_deliberation_task(task):
    """投资委员会审议"""
    pass

def invest_entering_task(task):
    """投资录入信息"""
    pass

def finance_riskowners_approve_task(task):
    """资金部负责人审批"""
    pass

def invest_data_check(task):
    """投资资料整理"""
    pass

def invest_application_task(task):
    """同业业务申请"""
    pass

def acceptance_lending_task(task):
    """签发审签"""
    pass

def acceptance_investigate_task(task):
    """签发预审"""
    pass

def acceptance_write_report_task(task):
    """签发撰写调查报告"""
    pass

def acceptance_subbranch_assessment_task(task):
    """签发支行风险评价"""
    pass

def acceptance_subbranch_review_task(task):
    """签发支行审查"""
    pass

def acceptance_subbranch_deliberation_task(task):
    """签发支行审贷小组审议"""
    pass

def acceptance_subbranch_president_task(task):
    """签发支行长审议"""
    pass

def acceptance_loan_application_task(task):
    """签发放款申请"""
    pass
def acceptance_ho_review_task(task):
    """签发总行信贷审查"""
    pass

def acceptance_riskowners_review_task(task):
    """签发信贷负责人审查"""
    pass

def acceptance_bm_review_task(task):
    """签发信贷分管行长审查"""
    pass

def acceptance_riskowners_chairman_review_task(task):
    """签发信贷负责人汇报董事长"""
    pass

def acceptance_committee_deliberation_task(task):
    """签发总行信贷委员会审议"""
    pass

def acceptance_ho_president_task(task):
    """签发总行行长审批"""
    pass

def acceptance_subbranch_approve_task(task):
    """签发支行长审批"""
    pass

def acceptance_credit_loan_task(task):
    """签发放款"""
    pass

def acceptance_ho_assessment_task(task):
    """签发总行风险评价"""
    pass

def acceptance_ho_riskowners_task(task):
    """签发风险负责人审查"""
    pass

def acceptance_subbranch_first_approve_task(task):
    """签发支行行长预审批"""
    pass

def acceptance_ho_review_approve_task(task):
    """签发信贷负责人审批"""
    pass

def extension_lendingproposition_task(task):
    """展期申请"""
    pass

def extension_investigate_task(task):
    """展期预审"""
    pass

def extension_write_report_task(task):
    """展期撰写调查报告"""
    pass

def extension_subbranch_assessment_task(task):
    """展期支行风险评价"""
    pass

def extension_subbranch_review_task(task):
    """展期支行审查"""
    pass

def extension_subbranch_deliberation_task(task):
    """展期支行审贷小组审议"""
    pass

def extension_subbranch_president_task(task):
    """展期支行长审议"""
    pass

def extension_loan_application_task(task):
    """展期放款申请"""
    pass
def extension_ho_review_task(task):
    """展期总行信贷审查"""
    pass

def extension_riskowners_review_task(task):
    """展期信贷负责人审查"""
    pass

def extension_bm_review_task(task):
    """展期信贷分管行长审查"""
    pass

def extension_riskowners_chairman_review_task(task):
    """展期信贷负责人汇报董事长"""
    pass

def extension_committee_deliberation_task(task):
    """展期总行信贷委员会审议"""
    pass

def extension_ho_president_task(task):
    """展期总行行长审批"""
    pass

def extension_subbranch_approve_task(task):
    """展期支行长审批"""
    pass

def extension_credit_loan_task(task):
    """展期放款"""
    pass

def extension_ho_assessment_task(task):
    """展期总行风险评价"""
    pass

def extension_ho_riskowners_task(task):
    """展期风险负责人审查"""
    pass

def extension_subbranch_first_approve_task(task):
    """展期支行行长预审批"""
    pass

def extension_ho_review_approve_task(task):
    """展期信贷负责人审批"""
    pass

def adjustment_loan_application_task(task):
    """授信调整申请"""
    pass
def adjustment_ho_review_approve_task(task):
    """授信调整信贷负责人审批"""
    pass
def adjustment_credit_loan_task(task):
    """授信调整放款"""
    pass



"""

并发等待任务：

    支行风险评价 : subbranch_assessment_gurad

    支行审查 : subbranch_review_gurad

"""
def activity_is_abort(flow, transaction_activity):
    session = get_session(transaction_activity)
    app_comment = session.query(ApplicationComment).filter(ApplicationComment.transaction_activity_id==transaction_activity.transaction_activity_id).first()
    logging.debug("comment_type:%s"%app_comment.comment_type)
    if app_comment.comment_type == u'同意':
        return True
    elif app_comment.comment_type is None:
        return True
    else:
        return False

def investigate_credit_application_gurad(flow,transaction_activity):
    """    贷款方向"""
    session = get_session(transaction_activity)
    comm = session.query(CommercialHouseCredit).filter(CommercialHouseCredit.transaction_id == transaction_activity.transaction_id).first()
    if comm:
        return False
    return True

def investigate_comm_application_gurad(flow,transaction_activity):
    """   转贷方向"""
    session = get_session(transaction_activity)
    comm = session.query(CommercialHouseCredit).filter(CommercialHouseCredit.transaction_id == transaction_activity.transaction_id).first()
    if comm:
        return True
    return False

def ticket_application_gurad(flow,transaction_activity):
    """贴现申请流转"""
    session = get_session(transaction_activity)
    app_tran = session.query(TransactionActivity).filter(TransactionActivity.transaction_activity_id==transaction_activity.transaction_activity_id).first()
    app = app_tran.transaction.application
    return app.product_code == '023'

def credit_application_gurad(flow,transaction_activity):
    """贷款申请流转"""
    session = get_session(transaction_activity)
    comm = session.query(CommercialHouseCredit).filter(CommercialHouseCredit.transaction_id == transaction_activity.transaction_id).first()
    if comm:
        return False
    app_tran = session.query(TransactionActivity).filter(TransactionActivity.transaction_activity_id==transaction_activity.transaction_activity_id).first()
    app = app_tran.transaction.application
    return app.product_code != '023'

def chc_credit_application_gurad(flow,transaction_activity):
    """转贷大表申请流转"""
    session = get_session(transaction_activity)
    comm = session.query(CommercialHouseCredit).filter(CommercialHouseCredit.transaction_id == transaction_activity.transaction_id).first()
    if comm:
        logging.debug("chc_credit_application_gurad 是转贷大表")
        return True
    return False

def subbranch_assessment_gurad(flow,transaction_activity):
    """支行风险评价流转"""
    session = get_session(transaction_activity)
    trans , act = session.query(TransactionActivity,Activity).filter(TransactionActivity.activity_id == Activity.activity_id, TransactionActivity.transaction_id == transaction_activity.transaction_id,Activity.activity_name == u"支行审查").first()
    return trans.finished

def subbranch_review_gurad(flow,transaction_activity):
    """支行审查流转"""
    session = get_session(transaction_activity)
    trans,act = session.query(TransactionActivity,Activity).filter(TransactionActivity.activity_id == Activity.activity_id, TransactionActivity.transaction_id == transaction_activity.transaction_id,Activity.activity_name == u"支行风险评价").first()
    return trans.finished

def discount_subbranch_assessment_gurad(flow,transaction_activity):
    """贴现支行风险评价流转"""
    session = get_session(transaction_activity)
    trans , act = session.query(TransactionActivity,Activity).filter(TransactionActivity.activity_id == Activity.activity_id, TransactionActivity.transaction_id == transaction_activity.transaction_id,Activity.activity_name == u"贴现支行审查").first()
    return trans.finished

def discount_subbranch_review_gurad(flow,transaction_activity):
    """贴现支行审查流转"""
    session = get_session(transaction_activity)
    trans,act = session.query(TransactionActivity,Activity).filter(TransactionActivity.activity_id == Activity.activity_id, TransactionActivity.transaction_id == transaction_activity.transaction_id,Activity.activity_name == u"贴现支行风险评价").first()
    return trans.finished

def acceptance_subbranch_assessment_gurad(flow,transaction_activity):
    """承兑汇票签发支行风险评价流转"""
    session = get_session(transaction_activity)
    trans , act = session.query(TransactionActivity,Activity).filter(TransactionActivity.activity_id == Activity.activity_id, TransactionActivity.transaction_id == transaction_activity.transaction_id,Activity.activity_name == u"签发支行审查").first()
    return trans.finished

def acceptance_subbranch_review_gurad(flow,transaction_activity):
    """承兑汇票签发支行审查流转"""
    session = get_session(transaction_activity)
    trans,act = session.query(TransactionActivity,Activity).filter(TransactionActivity.activity_id == Activity.activity_id, TransactionActivity.transaction_id == transaction_activity.transaction_id,Activity.activity_name == u"签发支行风险评价").first()
    return trans.finished

def ticket_approve_gurad(flow,transaction_activity):
    """验票岗流转"""
    session = get_session(transaction_activity)
    trans , act = session.query(TransactionActivity,Activity).filter(TransactionActivity.activity_id == Activity.activity_id, TransactionActivity.transaction_id == transaction_activity.transaction_id,Activity.activity_name == u"会计验票").first()
    return trans.finished

def accountant_approve_gurad(flow,transaction_activity):
    """会计岗流转"""
    session = get_session(transaction_activity)
    trans,act = session.query(TransactionActivity,Activity).filter(TransactionActivity.activity_id == Activity.activity_id, TransactionActivity.transaction_id == transaction_activity.transaction_id,Activity.activity_name == u"贴现验票").first()
    return trans.finished

def finance_invest_gurad(flow,transaction_activity):
    """财务部流转 投资类"""
    session = get_session(transaction_activity)
    trans,act = session.query(TransactionActivity,Activity).filter(TransactionActivity.activity_id == Activity.activity_id, TransactionActivity.transaction_id == transaction_activity.transaction_id,Activity.activity_name == u"风险负责人审查").first()
    return trans.finished

def riskowners_invest_gurad(flow,transaction_activity):
    """风险负责人流转 投资类"""
    session = get_session(transaction_activity)
    if invest_application_gurad(flow,transaction_activity) == False:
         return False
    else:
         trans,act = session.query(TransactionActivity,Activity).filter(TransactionActivity.activity_id == Activity.activity_id, TransactionActivity.transaction_id == transaction_activity.transaction_id,Activity.activity_name == u"财务部负责人审查").first()
         return trans.finished


def subbranch_deliberation_guard(flow,transaction_activity):
    """支行审议小组流转
    @Proposer   :郭强
        至少三人审议才能通过
    """
    session = get_session(transaction_activity)
    count = session.query(ApplicationComment).filter(ApplicationComment.transaction_activity_id==transaction_activity.transaction_activity_id).count()
    return count > 2

#ho_review_task                      总行信贷审查
#ho_assessment_task                  总行风险评价
#ho_riskowners_task                  风险负责人审查
#riskowners_review_task              信贷负责人审查
#bm_review_task                      信贷分管行长审查
#committee_deliberation_task         总行信贷委员会审议
#ho_president_task                   总行行长审批



def subbranch_amount_gurad(flow,transaction_activity):
    """支行权限流转
    @Proposer :郭强
      普通 金额小于200万
      转贷 金额小于400万
    """
    session = get_session(transaction_activity)
    trans,comm = session.query(Transaction,CommercialHouseCredit).outerjoin(CommercialHouseCredit,Transaction.transaction_id == CommercialHouseCredit.transaction_id).filter(Transaction.transaction_id == transaction_activity.transaction_id).first()
    if comm:
        return Decimal(trans.amount) <= Decimal(4000000)
    else:
        return Decimal(trans.amount) <= Decimal(2000000)

def acceptance_subbranch_amount_gurad(flow,transaction_activity):
    """承兑汇票签发支行权限流转
    """
    session = get_session(transaction_activity)
    app_tran = session.query(TransactionActivity).filter(TransactionActivity.transaction_activity_id==transaction_activity.transaction_activity_id).first()
    app = app_tran.transaction.application
    if app.bill_type == u'敞口':
        return False
    elif app.bill_type == u'全额':
        return True
    else:
       return False

def subbranch_prove_amount_gurad(flow,transaction_activity):
    """支行权限流转
    @Proposer :郭强
      普通 金额小于200万
      转贷 金额小于400万
    """
    session = get_session(transaction_activity)
    trans,comm = session.query(Transaction,CommercialHouseCredit).outerjoin(CommercialHouseCredit,Transaction.transaction_id == CommercialHouseCredit.transaction_id).filter(Transaction.transaction_id == transaction_activity.transaction_id).first()
    logging.debug("subbranch_prove_amount_gurad amount %s"%str(trans.amount));
    if comm:
        logging.debug("subbranch_prove_amount_gurad 是转贷大表");
        return False
    else:
        return Decimal(trans.amount) <= Decimal(2000000)

def acceptance_subbranch_prove_amount_gurad(flow,transaction_activity):
    """承兑汇票签发审批支行权限流转
    """
    session = get_session(transaction_activity)
    app_tran = session.query(TransactionActivity).filter(TransactionActivity.transaction_activity_id==transaction_activity.transaction_activity_id).first()
    app = app_tran.transaction.application
    if app.bill_type == u'敞口':
        return False
    elif app.bill_type == u'全额':
        return True
    else:
        return False

def ho_amount_gurad(flow,transaction_activity):
    """总行权限流转
      普通 金额大于200万
      转贷 金额大于400万
    """
    session = get_session(transaction_activity)
    trans,comm = session.query(Transaction,CommercialHouseCredit).outerjoin(CommercialHouseCredit,Transaction.transaction_id == CommercialHouseCredit.transaction_id).filter(Transaction.transaction_id == transaction_activity.transaction_id).first()
    if comm:
        return Decimal(trans.amount) > Decimal(4000000)
    else:
        return Decimal(trans.amount) > Decimal(2000000)

def acceptance_ho_amount_gurad(flow,transaction_activity):
    """承兑汇票签发总行权限流转
    """
    session = get_session(transaction_activity)
    app_tran = session.query(TransactionActivity).filter(TransactionActivity.transaction_activity_id==transaction_activity.transaction_activity_id).first()
    app = app_tran.transaction.application
    if app.bill_type == u'敞口':
        return True
    elif app.bill_type == u'全额':
        return False
    else:
        return True


def ho_review_gurad(flow,transaction_activity):
    """总行审查流转"""
    session = get_session(transaction_activity)
    trans = session.query(TransactionActivity,Activity).filter(TransactionActivity.activity_id == Activity.activity_id, TransactionActivity.transaction_id == transaction_activity.transaction_id,Activity.activity_name == "风险负责人审查").first()
    if trans:
         return trans.TransactionActivity.finished
    return Flase

def ho_assessment_gurad(flow,transaction_activity):
    """总行风险评价流转"""
    flag = invest_application_gurad(flow,transaction_activity)
    if flag:
        return False
    session = get_session(transaction_activity)
    trans , act = session.query(TransactionActivity,Activity).filter(TransactionActivity.activity_id == Activity.activity_id, TransactionActivity.transaction_id == transaction_activity.transaction_id,Activity.activity_name == "总行信贷审查").first()
    return trans.finished

def acceptance_ho_review_gurad(flow,transaction_activity):
    """承兑汇票签发总行审查流转"""
    session = get_session(transaction_activity)
    trans = session.query(TransactionActivity,Activity).filter(TransactionActivity.activity_id == Activity.activity_id, TransactionActivity.transaction_id == transaction_activity.transaction_id,Activity.activity_name == "签发风险负责人审查").first()
    if trans:
         return trans.TransactionActivity.finished
    return Flase

def acceptance_ho_assessment_gurad(flow,transaction_activity):
    """承兑汇票总行风险评价流转"""
    flag = invest_application_gurad(flow,transaction_activity)
    if flag:
        return False
    session = get_session(transaction_activity)
    trans , act = session.query(TransactionActivity,Activity).filter(TransactionActivity.activity_id == Activity.activity_id, TransactionActivity.transaction_id == transaction_activity.transaction_id,Activity.activity_name == "签发总行信贷审查").first()
    return trans.finished

def extension_ho_review_gurad(flow,transaction_activity):
    """展期总行审查流转"""
    session = get_session(transaction_activity)
    trans = session.query(TransactionActivity,Activity).filter(TransactionActivity.activity_id == Activity.activity_id, TransactionActivity.transaction_id == transaction_activity.transaction_id,Activity.activity_name == "展期风险负责人审查").first()
    if trans:
         return trans.TransactionActivity.finished
    return Flase

def extension_ho_assessment_gurad(flow,transaction_activity):
    """展期总行风险评价流转"""
    flag = invest_application_gurad(flow,transaction_activity)
    if flag:
        return False
    session = get_session(transaction_activity)
    trans , act = session.query(TransactionActivity,Activity).filter(TransactionActivity.activity_id == Activity.activity_id, TransactionActivity.transaction_id == transaction_activity.transaction_id,Activity.activity_name == "展期总行信贷审查").first()
    return trans.finished

def invest_application_gurad(flow,transaction_activity):
    """资金业务判断"""
    session = get_session(transaction_activity)
    app_tran = session.query(TransactionActivity).filter(TransactionActivity.transaction_activity_id==transaction_activity.transaction_activity_id).first()
    app = app_tran.transaction.application
    return app.product_code == '705'

def bank_application_gurad(flow,transaction_activity):
    """同业业务判断"""
    session = get_session(transaction_activity)
    app_tran = session.query(TransactionActivity).filter(TransactionActivity.transaction_activity_id==transaction_activity.transaction_activity_id).first()
    app = app_tran.transaction.application
    product = session.query(Product).filter(Product.product_code == app.product_code).first()
    return product.product_type_code == '91'

def bank_transfer_discount_application_gurad(flow,transaction_activity):
    """同业转贴现业务判断"""
    listp = ['808', '809', '811','812']
    session = get_session(transaction_activity)
    app_tran = session.query(TransactionActivity).filter(TransactionActivity.transaction_activity_id==transaction_activity.transaction_activity_id).first()
    app = app_tran.transaction.application
    product = session.query(Product).filter(Product.product_code == app.product_code).first()
    if product.product_type_code != '91':
        return False

    try:
        if listp.index(app.product_code) >= 0:
            return True
    except:
        return False

def bank_no_transfer_discount_application_gurad(flow,transaction_activity):
    """同业存放、拆解、同业存单、回购业务判断"""
    listp = ['801', '802', '803','804', '805', '806', '807','813','814']
    session = get_session(transaction_activity)
    app_tran = session.query(TransactionActivity).filter(TransactionActivity.transaction_activity_id==transaction_activity.transaction_activity_id).first()
    app = app_tran.transaction.application
    product = session.query(Product).filter(Product.product_code == app.product_code).first()
    if product.product_type_code != '91':
        return False

    try:
        if listp.index(app.product_code) >= 0:
            return True
    except:
        return False

def bank_bm_amount_gurad(flow,transaction_activity):
    """同业业务分管行长终审
        5亿总行行长审批
    """
    session = get_session(transaction_activity)
    app_tran = session.query(TransactionActivity).filter(TransactionActivity.transaction_activity_id==transaction_activity.transaction_activity_id).first()
    logging.debug("bank_bm_amount_gurad:%s"%str(app_tran.transaction.amount))
    if activity_is_abort(flow, transaction_activity) == True:
        return Decimal(app_tran.transaction.amount) < Decimal(500000000)
    else:
        return False

def bank_ho_amount_gurad(flow,transaction_activity):
    """同业业务总行行长终审
        5亿总行行长审批
    """
    session = get_session(transaction_activity)
    app_tran = session.query(TransactionActivity).filter(TransactionActivity.transaction_activity_id==transaction_activity.transaction_activity_id).first()
    logging.debug("bank_ho_amount_gurad:%s"%str(app_tran.transaction.amount))
    if activity_is_abort(flow, transaction_activity) == True:
        return Decimal(app_tran.transaction.amount) >= Decimal(500000000)
    else:
        return False

def discount_application_quote_report(flow,transaction_activity):
    """贴现是否引用调查报告"""
    session = get_session(transaction_activity)
    app_tran = session.query(TransactionActivity).filter(TransactionActivity.transaction_activity_id==transaction_activity.transaction_activity_id).first()
    if app_tran.transaction.application.quote_report == u'是':
        return True
    else:
        return False

def discount_application_no_quote_report(flow,transaction_activity):
    """贴现是否引用调查报告"""
    if discount_application_quote_report(flow,transaction_activity) == True:
        return False
    else:
        return True

def bank_application_no_abort(flow,transaction_activity):
    logging.info(u"bank_application_no_abort")
    if activity_is_abort(flow, transaction_activity) == True:
        logging.info(u"bank_application_no_abort True")
        return True
    else:
        logging.info(u"bank_application_no_abort False")
        return False
def bank_application_abort(flow,transaction_activity):
    logging.info(u"bank_application_abort")
    if activity_is_abort(flow, transaction_activity) == True:  #True为同意
        logging.info(u"bank_application_abort False")
        return False
    else:
        logging.info(u"bank_application_abort True")
        return True

def ho_review_task(self):
    """总行信贷审查"""
    logging.info(u"总行信贷审查")

def ho_assessment_task(self):
    """总行风险评价"""
    logging.info(u"总行风险评价")

def ho_riskowners_task(self):
    """风险负责人审查"""
    logging.info(u"风险负责人审查")

def riskowners_review_task(self):
    """信贷负责人审查"""
    logging.info(u"信贷负责人审查")

def bm_review_task(self):
    """信贷分管行长审查"""
    logging.info(u"信贷分管行长审查")

def committee_deliberation_task(self):
    """总行信贷委员会审议"""
    logging.info(u"总行信贷委员会审议")

def ho_president_task(self):
    """总行行长审批"""
    logging.info(u"总行行长审批")

def subbranch_first_approve_task(self):
    """支行行长初审"""
    logging.info(u"支行行长初审")

def ho_review_approve_task(self):
    """信贷负责人审批"""
    logging.info(u"信贷负责人审批")

def ho_approve_task(self):
    """总行行长终审"""
    logging.info(u"总行行长终审")
def bank_capital_charge_task(self):
    """资金部负责人同业业务审查"""
    logging.info(u"资金部负责人同业业务审查")

def invest_bm_review_task(self):
    """资金分管行长审查"""
    logging.info(u"资金分管行长审查")

def bank_application_task(self):
    """同业业务申请"""
    logging.info(u"同业业务申请")

def bank_review_task(self):
    """资金部同业业务风险审核"""
    logging.info(u"资金部同业业务风险审核")

def bank_bm_review_task(self):
    """同业分管行长审查"""
    logging.info(u"同业分管行长审查")

def branch_transfer_discount_task(self):
    """营业部转贴现审查"""
    logging.info(u"营业部转贴现审查")

def branch_transfer_discount_review_task(self):
    """营业部转贴现负责人审查"""
    logging.info(u"营业部转贴现负责人审查")

def bank_trade_data_check(self):
    """同业业务资料整理"""
    logging.info(u"同业业务资料整理")

def riskowners_chairman_review_task(self):
    """总行信贷审查人汇报董事长"""
    logging.info(u"总行信贷审查人汇报董事长")

def lending_discount_task(self):
    """贴现申请"""
    logging.info(u"贴现申请")

def discount_subbranch_review_task(self):
    """贴现支行审查"""
    logging.info(u"贴现支行审查")

def discount_info_input(self):
    """贴现信息录入"""
    logging.info(u"贴现信息录入")
def credit_granting_apply_task(self):
    """统一授信申请"""
    logging.info(u"统一授信申请")
def credit_granting_subbranch_deliberation_task(self):
    """授信支行审贷小组审议"""
    logging.info(u"授信支行审贷小组审议")
def credit_granting_subbranch_president_task(self):
    """授信支行长审议"""
    logging.info(u"授信支行长审议")
def ho_credit_granting_review_task(self):
    """总行授信审查"""
    logging.info(u"总行授信审查")
def credit_granting_committee_deliberation_task(self):
    """总行信贷委员会授信审议"""
    logging.info(u"总行信贷委员会授信审议")
def ho_credit_granting_president_task(self):
    """总行行长授信审批"""
    logging.info(u"总行行长授信审批")
def credit_granting_end_task(self):
    """统一授信查看"""
    logging.info(u"统一授信查看")
def credit_class_apply_task(self):
    """五级分类申请"""
    logging.info(u"五级分类申请")
def credit_class_subbranch_deliberation_task(self):
    """支行审贷小组五级分类审议"""
    logging.info(u"支行审贷小组五级分类审议")
def credit_class_subbranch_president_task(self):
    """支行长五级分类审议"""
    logging.info(u"支行长五级分类审议")
def ho_credit_class_review_task(self):
    """总行五级分类审查"""
    logging.info(u"总行五级分类审查")
def ho_credit_class_bm_review_task(self):
    """信贷分管行长五级分类审批"""
    logging.info(u"信贷分管行长五级分类审批")
def ho_credit_class_committee_deliberation_task(self):
    """总行信贷委员会五级分类审议"""
    logging.info(u"总行信贷委员会五级分类审议")
def ho_credit_class_president_task(self):
    """总行行长五级分类审批"""
    logging.info(u"总行行长五级分类审批")

def repossession_apply_task(self):
    """抵贷资产申请"""
    logging.info(u"抵贷资产申请")
def repossession_subbranch_deliberation_task(self):
    """支行审贷小组抵贷资产审议"""
    logging.info(u"支行审贷小组抵贷资产审议")
def repossession_subbranch_president_task(self):
    """支行长抵贷资产审议"""
    logging.info(u"支行长抵贷资产审议")
def repossession_finance_charge_task(self):
    """财务部负责人抵贷资产审查"""
    logging.info(u"财务部负责人抵贷资产审查")
def repossession_ho_riskowners_task(self):
    """风险负责人抵贷资产审查"""
    logging.info(u"风险负责人抵贷资产审查")
def repossession_ho_loan_charge_task(self):
    """信贷负责人抵贷资产审查"""
    logging.info(u"信贷负责人抵贷资产审查")
def repossession_ho_credit_bm_review_task(self):
    """信贷分管行长抵贷资产审批"""
    logging.info(u"信贷分管行长抵贷资产审批")
def repossession_ho_credit_bm_review_task(self):
    """信贷分管行长抵贷资产审批"""
    logging.info(u"信贷分管行长抵贷资产审批")
def repossession_ho_credit_committee_deliberation_task(self):
    """总行信贷委员会抵贷资产审议"""
    logging.info(u"总行信贷委员会抵贷资产审议")
def repossession_ho_credit_class_president_task(self):
    """总行行长抵贷资产审批"""
    logging.info(u"总行行长抵贷资产审批")
def invest_enering_review_task(self):
    """投资交易复核"""
    logging.info(u"投资交易复核")
def bank_ho_approve_task(self):
    """总行行长同业业务终审"""
    logging.info(u"总行行长同业业务终审")
def invest_ho_approve_task(self):
    """总行行长同业业务终审"""
    logging.info(u"总行行长同业业务终审")
def repossession_ho_assessment_task(self):
    """总行风险抵贷资产评价"""
    logging.info(u"总行风险抵贷资产评价")
def repossession_standingbook_task(self):
    """抵贷资产台账登记"""
    logging.info(u"抵贷资产台账登记")

'''
def application_assign(task):
    session = get_session(task)
    user_name = get_parameter(task.activity, u'用户')
    application = session.query(Application).filter(Application.transaction_id == task.transaction_id).first()
    #task.user = session.query(User).filter(User.user_name==user_name).one()
    logging.debug("session:%s"%str(session))

# 输入要素入库后，执行流程并转入下一步
def application(task):
    print "loan application assign func"
    session = get_session(task)
    application = session.query(Application).filter(Application.transaction_id == task.transaction_id).first()
    application.status = u'待预审核'
    session.commit()

def pre_examine(task):
    print "loan pre_examine assign func"
    session = get_session(task)
    application = session.query(Application).filter(Application.transaction_id == task.transaction_id).first()
    application.status = u'待支行审贷委审议'
    session.add_all([
        PendApprove(name=u'张委员', application_id = application.id, status=u'待审议'),
        PendApprove(name=u'李委员', application_id = application.id, status=u'待审议'),
        PendApprove(name=u'万委员', application_id = application.id, status=u'待审议'),
    ])
    session.commit()


def branch_review_committee(task):
    print "loan branch_review_committee assign func"
    session = get_session(task)
    application = session.query(Application).filter(Application.transaction_id == task.transaction_id).first()
    application.status = u'待支行长审批'
    session.commit()

def branch_manager_approve(task):
    print "loan branch_manager_approve assign func"
    session = get_session(task)
    application = session.query(Application).filter(Application.transaction_id == task.transaction_id).first()
    application.status = u'审批通过'
    session.commit()
'''



