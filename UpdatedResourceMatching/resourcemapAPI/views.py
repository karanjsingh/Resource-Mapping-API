from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from resourcemap.models import Resource,Project
from .serializers import ResourceSerializer,ProjectSerializer
from rest_framework import status
from django.http import HttpResponse, JsonResponse
# from rest_framework.views import APIView
from collections import deque
from datetime import datetime, date, timedelta
import logging

logger = logging.getLogger(__file__)

@api_view(['GET'])
def getData(request):
    items = Project.objects.all()
    serializer = ProjectSerializer(items,many=True)
    return Response(serializer.data)
    # once we pass the dictionary in Response the output is JSON data

@api_view(['GET'])
def getEmpData(request):
    items = Resource.objects.all()
    serializer = ResourceSerializer(items,many=True)
    return Response(serializer.data)
    
@api_view(['POST'])
def addresource(request):
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE','GET','PUT'])
def detailItem(request,pk):
    try:
        item = Project.objects.get(pk=pk)
    except Resource.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProjectSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProjectSerializer(item, data=request.data)
        print(request.data,Project.objects.values_list().get(pk=pk))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        item.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
def clear(request):
    p = Project.objects.all()
    for i in p:
        i.empid=None
        i.save()
    context = {"Data has been cleared": "Completed"}
    return JsonResponse(context)


def clear1():
    p = Project.objects.all()
    for i in p:
        i.empid=None
        i.save()
def updateDB(mapdic):
    clear1()
    for project in mapdic:
        for req in mapdic[project]:
            req_id = int(req['Request_id'])
            emp_id = req['EMP_ID']
            t = Project.objects.get(id=req_id)
            if not t.empid:
                t.empid = emp_id  # change field
            else:
                t.empid = t.empid + ", "+emp_id
            t.save() # this will update only


@api_view(['GET'])
def mapResource(request):
    # try:
        projects = Project.objects.all()
        resources = Resource.objects.all()
        p=projects.count()
        r=resources.count()
        # r=0
        if p==0:
            logger.info("Inside Map Resource and No project is available")
            return Response({'PROJECTS AVAILABILITY':'NO PROJECT IS AVAILABLE'},status=status.HTTP_204_NO_CONTENT)
        if r==0:
            logger.info("Inside Map Resource and No resource is available to map")
            return Response({'RESOURCES AVAILABILITY':'NO RESOURCE IS AVAILABLE TO MAP ON PROJECTS'},status=status.HTTP_204_NO_CONTENT)
        
        try:
            resource_skills = [i[0] for i in set(resources.values_list('skill'))]
        except Resource.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        resources_dict = {}
        logger.info("STARTED creating Resource Skill Dictionary")
        for skill in resource_skills:
            d = Resource.objects.filter(skill=skill)
            if skill in resources_dict:
                resources_dict[skill].append(list(d.values_list()))
            else:
                resources_dict[skill]=list(d.values_list())
        logger.info("CREATED Resource Skill Dictionary")
        # resourcesList = list(resources.values_list())
        projectsList = list(projects.values_list())
        # print((resourcesList[0][3]-resourcesList[0][4]).days<5)
        

        ## sort these projects acc to startdate
        logger.info("START SORTING PROJECT REQUIREMENTS ACCORDING TO START DATE")
        projectsList = sorted(projectsList, key=lambda x:x[5])
        projectsList = sorted(projectsList, key=lambda x:x[4])
        logger.info("SORTING COMPLETED")

        ## modify the date for each resource as you book 
        mapdic={}
        ## function will update and make new entry into the dictionary
        def updatemapdic(id,projectname,skillset,empid,stdate,endate,availability):
            logger.info("UPDATE the MAP Dictionary for PROJECT: {} and SkillSET: {} with EMPLOYEE: {} from {} to {}".format(projectname,skillset,empid,stdate,endate))
            if projectname in mapdic:
                mapdic[projectname].append({'Request_id':id,'SKILL':skillset,'Availablity':availability,'EMP_ID':empid,'START DATE':stdate,'END DATE':endate})
            else:
                mapdic[projectname]=[{'Request_id':id,'SKILL':skillset,'Availablity':availability,'EMP_ID':empid,'START DATE':stdate,'END DATE':endate}]
            logger.info("UPDATE COMPLETED")
        for id,projectname,skillset,_,stdate,endate in projectsList:
            if skillset in resources_dict:
                st = deque(resources_dict[skillset])
                count=0
                n=len(st)
                while st:
                    count+=1
                    if count>=n+1:
                        break
                    res = st.popleft()
                    resid,empid,resskill,resstdate,resendate = res
                    if resstdate<=stdate and resendate>=stdate:
                        ## when end date of project exactly match with end date of resource
                        if resendate==endate:   
                            updatemapdic(id,projectname,skillset,empid,stdate,endate,"YES")                                    
                            
                            up_stdate = resstdate
                            up_endate = stdate+timedelta(days=-1)
                            if up_stdate<=up_endate:
                                up_res = (resid,empid,resskill,up_stdate,up_endate)
                                st.append(up_res)
                            resources_dict[skillset] = st
                            break
                        ## when resource end date is bigger than project end date
                        elif resendate>endate:
                            updatemapdic(id,projectname,skillset,empid,stdate,endate,"YES")
                            
                            up_stdate = endate+timedelta(days=1)
                            up_endate = resendate
                            up_res = (resid,empid,resskill,up_stdate,up_endate)
                            st.append(up_res)
                            up_stdate = resstdate
                            up_endate = stdate+timedelta(days=-1)
                            if up_stdate<=up_endate:
                                up_res = (resid,empid,resskill,up_stdate,up_endate)
                                st.append(up_res)
                            resources_dict[skillset] = st
                            break
                        ## when project end date is bigger than resource end date. Now update the project start time and employee time as well
                        elif endate>resendate:
                            up_stdate = resstdate
                            up_endate = stdate+timedelta(days=-1)
                            if up_stdate<=up_endate:
                                up_res = (resid,empid,resskill,up_stdate,up_endate)
                                st.append(up_res)
                            resources_dict[skillset] = st
                            updatemapdic(id,projectname,skillset,empid,stdate,resendate,"YES")
                            
                            stdate=resendate+timedelta(days=1)
                            
                    else:
                        st.append(res)
                        resources_dict[skillset] = st
            else:
                updatemapdic(id,projectname,skillset,"NONE","NONE","NONE","NO RESOURCE IS AVAIABLE WITH MENTIONED SKILL")

        # return JsonResponse(mapdic,json_dumps_params={'indent': 2})
        updateDB(mapdic)
        return Response(mapdic)
    # except:
    #     content = {'DATABASE NAME OR ENTRIES ARE INVALID':"PLEASE RAISE THE TICKET"}
    #     logger.exception("DATABASE NAME OR ENTRIES ARE INVALID")
    #     return Response(content, status=status.HTTP_400_BAD_REQUEST)







