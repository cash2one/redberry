# coding: utf-8
__author__ = 'chengc017'
from DoctorSpring.util import constant,helper
from DoctorSpring.models import File ,Diagnose,User,DiagnoseLog,Comment,Doctor,Hospital
from DoctorSpring.models import UserRole
from database import db_session

#type fullFile代表查询文件返回文件全部信息，如果没有只返回FILE URL
def userCenterDiagnoses(diagnoses,type=None):
    if diagnoses is None or len(diagnoses)<1:
        return
    result=[]
    for diagnose in diagnoses:
        diagDict={}

        if hasattr(diagnose,"patient") and diagnose.patient and diagnose.patient.realname:
            diagDict['patientName']=diagnose.patient.realname
        if hasattr(diagnose,"doctor") and diagnose.doctor and diagnose.doctor.username:
            diagDict['doctorName']=diagnose.doctor.username
            if hasattr(diagnose.doctor,'hospital') and diagnose.doctor.hospital and diagnose.doctor.hospital.name:
                diagDict['doctorHispital']= diagnose.doctor.hospital.name

        if hasattr(diagnose,"hospital") and diagnose.hospital and diagnose.hospital.name:
            diagDict['hispital']=diagnose.hospital.name


        if diagnose.createDate:
            diagDict["date"]=diagnose.createDate.strftime('%Y-%m-%d')
        if diagnose.id:
            diagDict['id']=diagnose.id
        if diagnose.diagnoseSeriesNumber:
            diagDict['diagnosenumber']=diagnose.diagnoseSeriesNumber
        if diagnose.status or diagnose.status==0:
            diagDict['statusId']=diagnose.status
            diagDict['status']=constant.DiagnoseStatus.getStatusName(diagnose.status)
        dicomUrl=None
        otherUrls=None
        if diagnose.pathologyId:
            dicomUrl=File.getDicomFileUrl(diagnose.pathologyId,type)
            if dicomUrl:
                diagDict['hasDicom'] = True
            else:
                diagDict['hasDicom'] = False
            otherUrls=File.getFilesUrl(diagnose.pathologyId,type)
            if otherUrls:
                diagDict['hasDoc']=True
            else:
                diagDict['hasDoc']=False
        if type:
            diagDict['dicomUrl'] = parseFileUrl(dicomUrl)
            diagDict['docUrl']=parseFilesUrl(otherUrls)
        else:
            diagDict['dicomUrl'] = dicomUrl
            diagDict['docUrl']= otherUrls

        if hasattr(diagnose,'report') and diagnose.report and diagnose.report.fileUrl:
            diagDict['reportUrl']= diagnose.report.fileUrl


        if hasattr(diagnose,"pathology") and diagnose.pathology:
            pathology=diagnose.pathology
            if hasattr(pathology,"pathologyPostions") and pathology.pathologyPostions:
                pathologyPositons=pathology.pathologyPostions
                if pathologyPositons and len(pathologyPositons)>0:
                    positions=u''
                    for pathologyPositon in pathologyPositons:
                        position=pathologyPositon.position
                        positions+=(u' '+position.name)
                    diagDict['positionName']=positions
        #print diagDict['doctorName'],diagDict['positons']


        isFeedback=Comment.existCommentBydiagnose(diagnose.id,type=constant.CommentType.DiagnoseComment)
        diagDict['isFeedback']=isFeedback


        result.append(diagDict)

    return result

def parseFileUrl(fileUrlContainer):
    result = {}
    if fileUrlContainer:
        result['url'] = fileUrlContainer[0]
        result['name'] = fileUrlContainer[1]
        result['size'] = fileUrlContainer[2]
        result['id'] = fileUrlContainer[3]
    return result

def parseFilesUrl(fileUrlContainer):
    if fileUrlContainer and len(fileUrlContainer) > 0:
       resultArr = []
       for item in fileUrlContainer:
            resultArr.append(parseFileUrl(item))
       return resultArr
    return None


def getDiagnoseListByKefu(diagnoses):
    if diagnoses is None or len(diagnoses)<1:
        return
    result=[]
    for diagnose in diagnoses:
        diagDict={}

        if hasattr(diagnose,"patient") and diagnose.patient and diagnose.patient.realname:
            diagDict['patientName']=diagnose.patient.realname
        if hasattr(diagnose,"patient") and diagnose.patient:
            diagDict['mobile']=diagnose.patient.identityPhone
        if hasattr(diagnose,"doctor") and diagnose.doctor and diagnose.doctor.username:
            diagDict['doctorName']=diagnose.doctor.username
            if hasattr(diagnose.doctor,'hospital') and diagnose.doctor.hospital and diagnose.doctor.hospital.name:
                diagDict['doctorHispital']= diagnose.doctor.hospital.name

        if hasattr(diagnose,"hospital") and diagnose.hospital and diagnose.hospital.name:
            diagDict['hispital']=diagnose.hospital.name


        if diagnose.createDate:
            diagDict["date"]=diagnose.createDate.strftime('%Y-%m-%d')
        if diagnose.id:
            diagDict['id']=diagnose.id
        if diagnose.diagnoseSeriesNumber:
            diagDict['diagnosenumber']=diagnose.diagnoseSeriesNumber
        if diagnose.status or diagnose.status==0:
            diagDict['statusId']=diagnose.status
            diagDict['status']=constant.DiagnoseStatus.getStatusName(diagnose.status)
        if diagnose.pathologyId:
            dicomUrl=File.getDicomFileUrl(diagnose.pathologyId)
            if dicomUrl:
                diagDict['dicomUrl'] = dicomUrl
            otherUrls=File.getFilesUrl(diagnose.pathologyId)
            if otherUrls:
                diagDict['otherUrls']=otherUrls
        if hasattr(diagnose,'report') and diagnose.report and diagnose.report.fileUrl:
            diagDict['reportUrl']= diagnose.report.fileUrl


        if hasattr(diagnose,"pathology") and diagnose.pathology:
            pathology=diagnose.pathology
            postionLen=0
            if hasattr(pathology,"pathologyPostions") and pathology.pathologyPostions:
                pathologyPositons=pathology.pathologyPostions
                postionLen=len(pathologyPositons)
                if pathologyPositons and len(pathologyPositons)>0:
                    positions=u''
                    for pathologyPositon in pathologyPositons:
                        position=pathologyPositon.position
                        positions+=(u' '+position.name)
                    diagDict['positionName']=positions
            #print diagDict['doctorName'],diagDict['positons']
            if pathology.diagnoseMethod==constant.DiagnoseMethod.Mri:
                diagDict['payAmount']=diagnose.getPayCount(constant.DiagnoseMethod.Mri,postionLen,diagnose.getUserDiscount(diagnose.patientId))
                diagDict['diagnoseMethod']=constant.DiagnoseMethod.Mri
            elif pathology.diagnoseMethod==constant.DiagnoseMethod.Ct:
                diagDict['payAmount']=diagnose.getPayCount(constant.DiagnoseMethod.Ct,postionLen,diagnose.getUserDiscount(diagnose.patientId))
                diagDict['diagnoseMethod']=constant.DiagnoseMethod.Ct



        isFeedback=Comment.existCommentBydiagnose(diagnose.id,type=constant.CommentType.DiagnoseComment)
        diagDict['isFeedback']=isFeedback


        result.append(diagDict)

    return result


def getDiagnoseDetailInfo(diagnose):
    if diagnose is None:
        return
    diagDict={}
    diagDict['id']=diagnose.id
    if diagnose.diagnoseSeriesNumber:
        diagDict['diagnosenumber']=diagnose.diagnoseSeriesNumber
    if hasattr(diagnose,"patient") and diagnose.patient:
        if diagnose.patient.realname:
            diagDict['patientName']=diagnose.patient.realname
        if diagnose.patient.gender:
            diagDict['gender']=constant.Gender[diagnose.patient.gender]
        if diagnose.patient.birthDate:
            diagDict['birthDate']=diagnose.patient.birthDate.strftime('%Y-%m-%d')

    #diagDict['type']=diagnose.type
    if hasattr(diagnose,"doctor") and diagnose.doctor and diagnose.doctor.username:
        diagDict['doctorName']=diagnose.doctor.username
    if diagnose.createDate:
        diagDict["date"]=diagnose.createDate.strftime('%Y-%m-%d')

    # if hasattr(diagnose,"hospital") and diagnose.hospital:
    #     diagDict['hospitalHistory']=diagnose.hospital.name
    #     diagDict['hospitalId']=diagnose.hospitalId

    if diagnose.pathologyId:
        diagDict['dicomUrl']=File.getDicomFileUrl(diagnose.pathologyId)

    if diagnose.pathologyId:
        diagDict['docUrl']=File.getFilesUrl(diagnose.pathologyId)


    if hasattr(diagnose,"pathology") and diagnose.pathology:
        pathology=diagnose.pathology
        diagDict['caseHistory']=pathology.caseHistory
        diagDict['diagnoseType']=pathology.diagnoseMethod
        if hasattr(pathology,"pathologyPostions") and pathology.pathologyPostions:
            pathologyPositons=pathology.pathologyPostions
            if pathologyPositons and len(pathologyPositons)>0:
                positions=u''
                for pathologyPositon in pathologyPositons:
                    position=pathologyPositon.position
                    positions+=(u' '+position.name)
                diagDict['positionName']=positions
        if hasattr(pathology,"hospital") and pathology.hospital:
            diagDict['hospitalHistory']=pathology.hospital.name
            diagDict['hospitalId']=pathology.hospitalId

    if hasattr(diagnose,'report') and diagnose.report:
        diagDict['reportId']=diagnose.reportId
        diagDict['techDes']=diagnose.report.techDesc
        diagDict['imageDes']=diagnose.report.imageDesc
        diagDict['diagnoseResult']=diagnose.report.diagnoseDesc

    return diagDict

def getDiagnoseDetailInfoByPatient(session,diagnose):
    if diagnose is None:
        return
    diagDict={}
    diagDict['id']=diagnose.id
    if hasattr(diagnose,"patient") and diagnose.patient:
        if diagnose.patient.realname:
            diagDict['patientName']=diagnose.patient.realname
        if diagnose.patient.gender:
            diagDict['gender']=constant.Gender[diagnose.patient.gender]
        if diagnose.patient.birthDate:
            diagDict['birthDate']=diagnose.patient.birthDate.strftime('%Y-%m-%d')
    if diagnose.diagnoseSeriesNumber:
        diagDict['diagnosenumber']=diagnose.diagnoseSeriesNumber
    #diagDict['type']=diagnose.type
    if hasattr(diagnose,"doctor") and diagnose.doctor and diagnose.doctor.username:
        diagDict['doctorName']=diagnose.doctor.username
        diagDict['doctorUserId']=diagnose.doctor.userId
    if diagnose.createDate:
        diagDict["applyTime"]=diagnose.createDate.strftime('%Y-%m-%d')
    if diagnose.status:
        diagDict['diagnoseStatus']=diagnose.status
    # if hasattr(diagnose,"hospital") and diagnose.hospital:
    #     diagDict['hospitalHistory']=diagnose.hospital.name
    #     diagDict['hospitalId']=diagnose.hospitalId

    if diagnose.pathologyId:
        diagDict['dicomUrl']=File.getDicomFileUrl(diagnose.pathologyId)

    if diagnose.pathologyId:
        diagDict['docUrl']=File.getFilesUrl(diagnose.pathologyId)


    if hasattr(diagnose,"pathology") and diagnose.pathology:
        pathology=diagnose.pathology
        diagDict['caseHistory']=pathology.caseHistory
        diagDict['diagnoseType']=pathology.diagnoseMethod
        if hasattr(pathology,"pathologyPostions") and pathology.pathologyPostions:
            pathologyPositons=pathology.pathologyPostions
            if pathologyPositons and len(pathologyPositons)>0:
                positions=u''
                for pathologyPositon in pathologyPositons:
                    position=pathologyPositon.position
                    positions+=(u' '+position.name)
                diagDict['positionName']=positions

        if hasattr(pathology,"hospital") and pathology.hospital:
            diagDict['hospitalHistory']=pathology.hospital.name
            diagDict['hospitalId']=pathology.hospitalId

    if hasattr(diagnose,'report') and diagnose.report and diagnose.report.fileUrl:
        diagDict['reportId']=diagnose.reportId
        diagDict['reportUrl']= diagnose.report.fileUrl
        # diagDict['techDes']=diagnose.report.techDesc
        # diagDict['imageDes']=diagnose.report.imageDesc
        # diagDict['diagnoseResult']=diagnose.report.diagnoseDesc

    diagnoseLogs=DiagnoseLog.getDiagnoseLogByDiagnoseId(session,diagnose.id)
    diagnoseLogsDict=getDiagnoseLogsDict(diagnoseLogs)
    if diagnoseLogs and len(diagnoseLogs)>0:
        diagDict['actions']=diagnoseLogsDict
    isFeedback=Comment.existCommentBydiagnose(diagnose.id,type=constant.CommentType.DiagnoseComment)
    diagDict['isFeedback']=str(isFeedback)

    return diagDict

def getDiagnoseLogsDict(diagnoseLogs):
    if diagnoseLogs is None or len(diagnoseLogs)<1:
        return None
    results=[]
    for diagnoseLog in diagnoseLogs:
        resultDict={}
        resultDict['id']=diagnoseLog.id
        if diagnoseLog.createTime:
            resultDict['time']=diagnoseLog.createTime.strftime('%Y-%m-%d')
        if diagnoseLog.action:
            resultDict['title']=diagnoseLog.action
        if diagnoseLog.description:
            resultDict['comments']=diagnoseLog.description
        if hasattr(diagnoseLog,'user') and diagnoseLog.user and diagnoseLog.user.name:
            resultDict['name']=diagnoseLog.user.name
        results.append(resultDict)
    return results

def getDiagnosePositonFromDiagnose(diagnose):
    if diagnose is None:
        return
    if hasattr(diagnose,"pathology") and diagnose.pathology:
        pathology=diagnose.pathology
        if hasattr(pathology,"pathologyPostions") and pathology.pathologyPostions:
            pathologyPositons=pathology.pathologyPostions
            if pathologyPositons and len(pathologyPositons)>0:
                positions=u''
                for pathologyPositon in pathologyPositons:
                    position=pathologyPositon.position
                    positions+=(u' '+position.name)
                return positions

def getDoctorNeedDiagnoseMessageContent(diagnose,doctor):
    content=' 您好，系统中有一个新到的影像需要您来诊断！'
    if doctor.username:
        content=doctor.username+content
    diagnoseContent=u''
    if diagnose.diagnoseSeriesNumber:
        diagnoseContent=" 诊断号:"+diagnose.diagnoseSeriesNumber

    if hasattr(diagnose,"patient") and diagnose.patient:
        if diagnose.patient.realname:
            diagnoseContent+=' | 患者:'+diagnose.patient.realname

    if hasattr(diagnose,"pathology") and diagnose.pathology:
        pathology=diagnose.pathology
        if pathology.diagnoseMethod:
            diagnoseContent+=' | 诊断类型:'+pathology.diagnoseMethod
        if pathology and hasattr(pathology,"pathologyPostions") and pathology.pathologyPostions:
            pathologyPositons=pathology.pathologyPostions
            if pathologyPositons and len(pathologyPositons)>0:
                positions=u''
                for pathologyPositon in pathologyPositons:
                    position=pathologyPositon.position
                    if position and position.name:
                        positions+=(u' '+position.name)
                diagnoseContent+=' | 诊断部位:'+positions
        content+=diagnoseContent
    return content
def getPatienDiagnoseMessageContent(diagnose,content=None):
    if content is None:
        content=' 您好，系统中有一个影像已被处理，请查看处理结果！'
    #content=' 您好，系统中有一个新到的影像需要您来诊断！'
    if diagnose and hasattr(diagnose,'patient') and hasattr(diagnose.patient,'user') and diagnose.patient.user:
        content=diagnose.patient.user.name+content
    diagnoseContent=u''
    if diagnose.diagnoseSeriesNumber:
        diagnoseContent=" 诊断号:"+diagnose.diagnoseSeriesNumber

    if hasattr(diagnose,"patient") and diagnose.patient:
        if diagnose.patient.realname:
            diagnoseContent+=' | 患者:'+diagnose.patient.realname

    if hasattr(diagnose,"pathology") and diagnose.pathology:
        pathology=diagnose.pathology
        if pathology.diagnoseMethod:
            diagnoseContent+=' | 诊断类型:'+pathology.diagnoseMethod
        if hasattr(pathology,"pathologyPostions") and pathology.pathologyPostions:
            pathologyPositons=pathology.pathologyPostions
            if pathologyPositons and len(pathologyPositons)>0:
                positions=u''
                for pathologyPositon in pathologyPositons:
                    position=pathologyPositon.position
                    if position and position.name:
                        positions+=(u' '+position.name)
                diagnoseContent+=' | 诊断部位:'+positions
        content+=diagnoseContent
    return content




def setDiagnoseCommentsDetailInfo(diagnoseCommentsDict):
    if diagnoseCommentsDict is None or len(diagnoseCommentsDict)<1:
        return
    for diagnoseComment in diagnoseCommentsDict:
        if diagnoseComment.has_key('observer'):
           observer=diagnoseComment.get('observer')
           user=User.getById(observer)
           if user:
              diagnoseComment['avatar']=user.imagePath
              diagnoseComment['senderName']=user.name

        if diagnoseComment.has_key('receiver'):
            receiver=diagnoseComment.get('receiver')
            user=User.getById(receiver)
            if user:
                #diagnoseComment['receiverName']=user.name
                doctor=Doctor.getByUserId(receiver)
                if doctor and hasattr(doctor,"hospital") and doctor.hospital :
                    diagnoseComment['doctorUserId']=receiver
                    diagnoseComment['hospitalId']= doctor.hospitalId
                    diagnoseComment['hospitalName']=doctor.hospital.name
                    diagnoseComment['receiverName']=doctor.username

        if diagnoseComment.has_key('diagnoseId'):
            diagnose=Diagnose.getDiagnoseById(diagnoseComment.get('diagnoseId'))
            if diagnose:
                if diagnose.score:
                    diagnoseComment['scoreName']=constant.DiagnoseScore[diagnose.score]
                # if diagnose.hospitalId and hasattr(diagnose,'hospital') and diagnose.hospital and diagnose.hospita.name:
                #     diagnoseComment['hospitalId']= diagnose.hospitalId
                #     diagnoseComment['hospitalName']=diagnose.hospital.name
                if hasattr(diagnose,"pathology") and diagnose.pathology:
                    pathology=diagnose.pathology
                    if hasattr(pathology,"pathologyPostions") and pathology.pathologyPostions:
                        pathologyPositons=pathology.pathologyPostions
                        if pathologyPositons and len(pathologyPositons)>0:
                            positions=u''
                            for pathologyPositon in pathologyPositons:
                                position=pathologyPositon.position
                                positions+=(u' '+position.name)
                            diagnoseComment['positionName']=positions


def setThanksNoteDetail(thanksNoteDicts):
    if thanksNoteDicts and len(thanksNoteDicts)<1:
        return
    for thanksNoteDict in thanksNoteDicts:
        if thanksNoteDict.has_key('sender'):
            observer=thanksNoteDict.get('sender')
            user=User.getById(observer)
            if user:
                thanksNoteDict['observer']=observer
                thanksNoteDict['observerName']=user.name
                if user.imagePath:
                    thanksNoteDict["avatarUrl"] = user.imagePath

def get_doctors_dict(doctors, pageno=1, count=1):
    if doctors is None:
        return
    result_Dict = {}
    result_Dict['currentPage'] = pageno
    result_Dict['pageNumber'] = count
    result = []
    for doctor in doctors:
        doctorDict = get_doctor(doctor)
        result.append(doctorDict)
    result_Dict['doctor'] = result
    return result_Dict




def get_doctor(doctor):
    if doctor is None:
        return
    doctorDict = {}
    if doctor.id:
        doctorDict['id'] = doctor.id

    if doctor.identityPhone:
        doctorDict['identityPhone']=doctor.identityPhone
    if hasattr(doctor, "username") and doctor.username:
        doctorDict['doctorname'] = doctor.username
        doctorDict['username'] = doctor.username
    if hasattr(doctor, "title") and doctor.title:
        doctorDict["doctortitle"] = doctor.title
    if hasattr(doctor, "doctorSkills") and len(doctor.doctorSkills) >= 1:
        skill_des = ''
        for skill in doctor.doctorSkills:
            if skill.skill:
                skill_des = skill_des + skill.skill.name + ', '
        doctorDict["skill"] = skill_des
    if hasattr(doctor, "hospital") and hasattr(doctor.hospital, "name") and doctor.hospital.name:
        doctorDict["hospitalname"] = doctor.hospital.name
    if hasattr(doctor, "department") and hasattr(doctor.department, "name") and doctor.department.name:
        doctorDict["departmentname"] = doctor.department.name
    if hasattr(doctor, "diagnoseCount") and doctor.diagnoseCount:
        doctorDict["diagnoseNumber"] = doctor.diagnoseCount
    if hasattr(doctor, "feedbackCount") and doctor.feedbackCount:
        doctorDict["goodFeedbackNumber"] = doctor.feedbackCount
    if hasattr(doctor, "user") and hasattr(doctor.user, "imagePath") and doctor.user.imagePath:
        doctorDict["avatarUrl"] = doctor.user.imagePath
    if  doctor.userId:
        doctorDict["userId"] = doctor.userId

    return doctorDict
def getUserFavoritiesDict(userFavorities):
    if userFavorities is None or len(userFavorities)<1:
        return None
    results=[]
    for userFav in userFavorities:
        resultDict={}
        if userFav.id:
            resultDict['id']=userFav.id
        if userFav.doctorId:
            resultDict['doctorId']=userFav.doctorId
        if hasattr(userFav,'doctor') and userFav.doctor and userFav.doctor.username:
            resultDict['name']=userFav.doctor.username
            content=u''
            if hasattr(userFav.doctor,'hospital') and userFav.doctor.hospital:
                content+=userFav.doctor.hospital.name
            if hasattr(userFav.doctor,'department') and userFav.doctor.department:
                content+='----'
                content+=userFav.doctor.department.name
            resultDict['content']=content


        if hasattr(userFav,'doctor') and userFav.doctor and userFav.doctor.userId:
            resultDict['uid']=userFav.doctor.userId
        if userFav.hospitalId:
            resultDict['uid']=userFav.hospitalId
        if userFav.docId:
            resultDict['uid']=userFav.docId
        #if userFav.type:
        resultDict['type']=userFav.type

        results.append(resultDict)
    return results


def get_patient(patient):
    if patient is None:
        return
    patientDict = {}
    if patient.id:
        patientDict['id'] = patient.id
    if hasattr(patient, "realname") and patient.realname:
        patientDict['name'] = patient.realname
    if hasattr(patient, "gender") and patient.gender:
        if patient.gender == 1:
            patientDict["gender"] = '男'
        else:
            patientDict["gender"] = '女'
    if hasattr(patient, "birthDate") and patient.birthDate:
        patientDict['birthdate'] = patient.birthDate.strftime("%Y-%m-%d")
    if hasattr(patient, "identityCode") and patient.identityCode:
        patientDict['identitynumber'] = patient.identityCode
    if hasattr(patient, "identityPhone") and patient.identityPhone:
        patientDict['phonenumber'] = patient.identityPhone

    patientDict['location'] = '陕西 西安'
    return patientDict


def get_pathology_list(pathologys):
    if len(pathologys) < 1:
        return
    results=[]
    for pathology in pathologys:
        pathologyDict={}
        pathologyDict['id'] = pathology.id
        if hasattr(pathology, "name") and pathology.name:
            pathologyDict['name'] = pathology.name

        results.append(pathologyDict)

    return results

def get_pathology(pathology):
    pathologyDict={}
    pathologyDict['id'] = pathology.id
    pathologyDict['dicomFile'] = getDocomFileName(pathology.id)
    if hasattr(pathology, "diagnoseMethod") and pathology.diagnoseMethod:
        pathologyDict['type'] = pathology.diagnoseMethod


    if hasattr(pathology, "pathologyPostions") and len(pathology.pathologyPostions) >= 1:
        positions = ''
        for position in pathology.pathologyPostions:
            if position.position:
                positions = positions + position.position.name + ', '
        pathologyDict["position"] = positions
    dicomUrl = File.getDicomFileUrl(pathology.id)
    pathologyDict["dicomUrl"] = dicomUrl

    return pathologyDict

def getDocomFileName(pathologyId):
    if pathologyId is None:
        return
    files=File.getFiles(pathologyId,constant.FileType.Dicom)
    if files and len(files):
        return files[0].name

def getFilesResult(files):
    if files is None or len(files)<1:
        return None
    fileResults=[]
    for file in files:
        fileResult={}
        fileResult['name']=file.name
        fileResult['type']=file.type
        fileResult['url']=file.url
        fileResults.append(fileResult)
    return fileResults
def getAccountInfo(userDict):
    if userDict is None:
        return
    doctor=Doctor.getByUserId(userDict.get('id'))
    if doctor:
        if doctor.identityPhone:
            userDict['identityPhone']=doctor.identityPhone
        if doctor.hospital and doctor.hospital.name:
            userDict['hospitalName']=doctor.hospital.name

        return userDict
    return None
def setConsultsResult(consutsDict, userId=0):
    if consutsDict is None:
        return
    for consutDict in consutsDict:
        type=consutDict.get('type')
        if type==1:
            if consutDict.get('doctorId'):
                    doctor=Doctor.getById(consutDict.get('doctorId'))
                    if doctor:
                        consutDict['doctorName']=doctor.username
                        consutDict['doctorTitle']=doctor.title
                        if hasattr(doctor,'user') and doctor.user and doctor.user.imagePath:
                            consutDict['avartarUrl']= doctor.user.imagePath
                    consutDict["statusText"] = getStatusText(consutDict.get("status"),
                                                             UserRole.checkRole(db_session,userId,constant.RoleId.Doctor))

        if type==0:
            if consutDict.get('userId'):
                user=User.getById(consutDict.get('userId'))
                if user:
                    consutDict['userName']=user.name
                    consutDict['avartarUrl']=user.imagePath
                    consutDict["statusText"] = getStatusText(consutDict.get("status"),
                                                             UserRole.checkRole(db_session,userId,constant.RoleId.Doctor))
        consutDict['amount']=consutDict.get('count')

def getStatusText(status, role):
    if status == constant.ConsultStatus.Unread:
        return u"未读咨询"
    if status == constant.ConsultStatus.Read:
        return u"已读咨询"
    if status == constant.ConsultStatus.PatientComments:
        if not role:
            return u"已读咨询"
        else:
            return u"有新回复"
    if status == constant.ConsultStatus.DoctorComments:
        if role:
            return u"已读咨询"
        else:
            return u"有新回复"
    return u"已读咨询"
def getAllHospital(hospitals):
    if hospitals is None or len(hospitals)<1:
        return
    result=[]

    for hospital in hospitals:
        hospitalDict={}
        hospitalDict['id']=hospital.id
        if hospital.name:
            hospitalDict['name']=hospital.name
        result.append(hospitalDict)

    return result


def getAllDepartments(departments):
    if departments is None or len(departments)<1:
        return
    result=[]

    for department in departments:
        departmentDict={}
        departmentDict['id']=department.id
        if department.name:
            departmentDict['name']=department.name
        result.append(departmentDict)

    return result



def getAllSkills(skills):
    if skills is None or len(skills)<1:
        return
    result=[]

    for skill in skills:
        skillDict={}
        skillDict['id']=skill.id
        if skill.name:
            skillDict['name']=skill.name
        result.append(skillDict)

    return result



