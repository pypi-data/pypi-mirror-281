from flask import Blueprint
from flask_apispec.views import MethodResource
from flask_apispec import doc, marshal_with, use_kwargs, FlaskApiSpec
from flask_restful import Api, Resource
import random,math
from app.eluent_curve.schemas import *
from datetime import datetime,timedelta
from dateutil import parser  # 需要安装 python-dateutil 库

eluent_curve_blue = Blueprint('eluent_curve_blue', __name__)
api = Api(eluent_curve_blue)

# 设定波形的周期和振幅
period = 60  # 波形的周期
amplitude = 100  # 波形的振幅
# 初始化波形的相位
phase = random.uniform(0, 2*math.pi)
phase_increment = (2 * math.pi) / period
@doc(tags=[" Get Eluent Curve"])
class GetCurveAPI(MethodResource, Resource):
    @use_kwargs(curveInPut, location='json')
    @marshal_with(curveOutPut)
    def post(self,**kwargs):
        global phase
        random_number = math.sin(phase)
        phase +=  (2 * math.pi) / period  # 控制波形移动的速度
        random_number = (random_number + 1) / 2 * 100 # 将值映射到0到1之

        start_time = parser.parse(kwargs['start_time'])
        current_time = datetime.now()
        time_elapsed = current_time - start_time
        time_str = str(timedelta(seconds=int(time_elapsed.total_seconds())))

        point = {
            "time":time_str,
           "value": random_number
        }
        print(point)
        return {"message": "People Refilling tasks successfully",
             "point":point
              }
current_id = 1
@doc(tags=[" Get Eluent Vertical"])
class GetVerticalAPI(MethodResource, Resource):
    @use_kwargs(curveInPut, location='json')
    @marshal_with(verticalOutPut)
    def post(self,**kwargs):
        global current_id
        current_time = datetime.now()
        start_time = parser.parse(kwargs['start_time'])
        time_elapsed = current_time - start_time
        timeStart = time_elapsed - timedelta(seconds=10)
        timeEnd = time_elapsed - timedelta(seconds=6)
        current_id += 1
        point = {
            "timeStart":timeStart,
            "timeEnd":timeEnd,
            "tube":current_id

        }
        return {"message": "People Refilling tasks","point":point}


@doc(tags=[" Get Eluent Line"])
class GetLinelAPI(MethodResource, Resource):

    @marshal_with(lineOutPut)
    def get(self,):
        point = []
        current_id_line = 1

        time = timedelta(seconds=0)
        for i in range(4):
            time = time + timedelta(seconds=30)
            current_id_line += 10
            value = current_id_line
            formatted_time = (datetime.min + time).strftime('%H:%M:%S')

            point.append({"time":formatted_time,"value":value})
        for i in range(4):
            time = time + timedelta(seconds=30)
            value = current_id_line
            formatted_time = (datetime.min + time).strftime('%H:%M:%S')
            point.append({"time": formatted_time, "value": value})
        print("point",point)
        return {"message": "People Refilling tasks","point":point}



def eluent_curve_api(docs):
    api.add_resource(GetCurveAPI, '/get_curve')
    docs.register(GetCurveAPI, blueprint="eluent_curve_blue")
    api.add_resource(GetVerticalAPI, '/get_vertical')
    docs.register(GetVerticalAPI, blueprint="eluent_curve_blue")
    api.add_resource(GetLinelAPI, '/get_line')
    docs.register(GetLinelAPI, blueprint="eluent_curve_blue")
