VBoxManage startvm "Kali-Pentest" --type gui



ssh kali@192.168.18.152


VBoxManage startvm "Kali-Pentest" --type headless


VBoxManage startvm "Kali-Pentest" --type headless && sleep 15 && ssh kali@192.168.18.152


VBoxManage controlvm "Kali-Pentest" poweroff && sleep 3 && VBoxManage startvm "Kali-Pentest" --type headless