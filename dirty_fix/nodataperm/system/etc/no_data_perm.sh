#!/system/bin/sh

focusedAppPkg=""

while true; do
        newFocus=$(dumpsys window | grep 'mCurrentFocus' | awk -F'[ /}]' '{print $(NF-2)}')
        if [ "$newFocus" != "" ] && [ "$newFocus" != "$focusedAppPkg" ]; then
            	focusedAppPkg="$newFocus"
         	log -t nodataperm "focus on: $focusedAppPkg"
	chmod 777 -R /sdcard/Android
	chmod 777 -R /data/media/0/Android 
	chmod 777 -R /sdcard/Android/data
	chmod 777 -R /data/media/0/Android/obb 
	chmod 777 -R /mnt/*/*/*/*/Android/data
	chmod 777 -R /mnt/*/*/*/*/Android/obb
              log -t nodataperm "chmod done"
        fi
        sleep 1
done
