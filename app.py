from flask import Flask
from flask import request,url_for
from flask import render_template
from fileinput import filename
import os
from flask import redirect,send_from_directory
from datetime import datetime



app=Flask(__name__)



@app.route("/",methods=['GET'])
def server_status():
    
    return {"message":"server is running successfully".title(),"status":200}


@app.route("/repackager/home/")
def home():
    status = request.args.get('status', 'upload the file')
    
    if status not in ["please enter the file extension !!",'upload the file','please enter the file name !!','successfully uploaded the file','please select and uploaded the file !!'] or len(status)<=0 or status is None:
        return redirect("/repackager/home/")
    
    return render_template("index.html",status=status.title())


@app.route("/repackager/home/files/upload/",methods=['GET',"POST"])
def upload():
    try:
        if request.method=="GET":
        
            return {"message":"this is a repackager file upload server".title(),"status":200} 
        
        elif request.method=="POST":

            #validating the input file name
            file_name = request.form.get('file_name', 'default_name')
            get_file_extension = request.form.get('file_extension', '')            
         
            if len(file_name)<=0:
                print("jj")
                return redirect("/repackager/home/?status=please enter the file name !!")
            
            if len(get_file_extension)<=0:
                
                return redirect("/repackager/home/?status=please enter the file extension !!")

            folder_name="EmergencyAlertsMediaFiles/"
            file=request.files['file']
            #end
            
            #creating the directory if not exists
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            #end
            
            
            #saving the input file
            file.save(f"{folder_name}/{file.filename}")
            #end
            
            #renaming the file
            os.rename(f"{folder_name}/{file.filename}",f"{folder_name}/{file_name}.{get_file_extension}")

            

            return redirect("/repackager/home/?status=successfully uploaded the file")
        
    except PermissionError:
        return redirect("/repackager/home/?status=please select and uploaded the file !!")

@app.route("/repackager/home/view_uploaded_contents/")
def view_uploded_contents():
    
    folder_name="EmergencyAlertsMediaFiles/"

    data=os.listdir(folder_name)
    
    final_data=[]
    
    index=1
    
    for fls in data:
        
        ff=os.path.getmtime(f"{folder_name}/{fls}")
        
        final_data.append({"cdn_link":f"/repackager/cdn/{fls}","no":index,"file_name":fls.split(".")[0],"file":fls,"uploaded_date":str(datetime.fromtimestamp(ff))})
        index+=1
    
    #print(final_data)
    
    return render_template("uploaded_contents.html",data=final_data)

@app.route("/repackager/home/delete_uploaded_contents/")        
def delete_uploaded_contents():
    file_name = request.args.get('file_name', 'default_name')            
    folder_name="EmergencyAlertsMediaFiles/"
    
    if len(file_name)>0:
        
        os.remove(f"{folder_name}/{file_name}")
    
    return redirect("/repackager/home/view_uploaded_contents/")


@app.route("/repackager/cdn/<file_name>")
def cdn(file_name):
    return send_from_directory("EmergencyAlertsMediaFiles",file_name)

if __name__=="__main__":
    #host="10.80.40.145"
    app.run(debug=True)