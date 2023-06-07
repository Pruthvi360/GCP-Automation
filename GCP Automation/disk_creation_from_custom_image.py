import subprocess,csv,time

data = [['Image Name','Disk Size'],['tata-hybrid-vprod',''], ['versa-poc-large-vprod',''],['versapoc2-basic-simple-cloud-prod-latest-1323042021',''],['versa-poc-small-vprod',''],['aar-tata-salesdemo-v59',''],['versa-security-salesdemo-v2',''],['tata-ciscosalesdemo-new-v9',''],['versa-sdwan-salesdemo-v12',''],['tata-ciscosalesdemo-new-dev-v11',''],['versa-sdwan-salesdemo-tcx-v29',''],['tata-ciscosalesdemo-new-v9','']]
def write_data():
    fo = open('custom-image-list.csv','w',newline='')
    cswr = csv.writer(fo, delimiter=',')
    for line in data:
            cswr.writerow(line)
    print("Writing Image name to the CSV file.....")
    time.sleep(2)
    fo.close()    
    return None

def get_disk_size_of_image():
    fr = open('custom-image-list.csv','r')
    custom_image_list = csv.reader(fr, delimiter=',')
    header = next(custom_image_list)
    for image in custom_image_list:        
            cmd_disk_size = f'gcloud compute images describe {image[0]}'
            print(cmd_disk_size)          
            sp1 = subprocess.Popen(cmd_disk_size, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            rc = sp1.wait()
            print(f' This is an status of execution code : {rc}')
            output,Error=sp1.communicate()
            if rc == 0:
                for each in output.splitlines():
                    if 'diskSizeGb' in each:
                        disk_size = each.split()[1]
                        print(f'{image[0]} : {disk_size}')
                        image_data = [image[0],disk_size[1:4]]
                        fw = open('custom-image-list-final.csv','w',newline='')
                        cswr = csv.writer(fw, delimiter=',')
                        cswr.writerow(image_data)
                        print("Writing Image name to the CSV file.....")
                        time.sleep(2)
                        fw.close()  
                #print(f'This is an output of :\n {output}')
            elif rc !=0:
                    print(f'This is an error output :\n {Error}')
    fr.close()                
        
def create_disk_from_image():
    fr = open('custom-image-list-final.csv','r')
    custom_image_list = csv.reader(fr, delimiter=',')
    for image in custom_image_list: 
        cmd = f"gcloud compute disks create {image[0]} --project=criterion-internal-prod --type=pd-balanced --size={image[1]}GB --zone=us-central1-a --image={line} --image-project=criterion-internal-prod"
        sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        rc = sp.wait()
        print(f' This is an status of execution code : {rc}')
        output,Error=sp.communicate()
        print(f'This is an output of :\n {output}')
        if rc !=0:
            print(f'This is an error output :\n {Error}')
    
def main():
    write_data()
    get_disk_size_of_image()
    create_disk_from_image()       
    
if __name__ == "__main__":
    main()