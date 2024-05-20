### Config GoSungrow

Resources:
https://github.com/MickMake/GoSungrow
https://gist.github.com/Paraphraser/cad3b0aa6428c58ee87bc835ac12ed37


#### Config appkey and host
```
./bin/darwin_arm64/GoSungrow config write --appkey=B0455FBE7AA0328DB57B59AA729F05D8 --host=https://gateway.isolarcloud.eu
```

#### Add your username and password to the config. (See [the website](https://web3.isolarcloud.eu/))
Once done, it's a case of set and forget. GoSungrow will handle the re-authentication for you.
```
./bin/darwin_arm64/GoSungrow config write --user=USERNAME --password=PASSWORD
```

#### Login to SunGrow website.
```
./bin/darwin_arm64/GoSungrow api login
```

#### Get the list of devices
```
./bin/darwin_arm64/GoSungrow show ps list
```
Copy the Ps ID of the device you want to monitor (second column, e.g. 1234567)

```
(.venv) ➜  smart_charge ./bin/darwin_arm64/GoSungrow show ps list
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Ps Key           ┃ Ps Id   ┃ Device Type ┃ Device Code ┃ Channel Id ┃ Serial #    ┃ Factory Name ┃ Device Model ┃
┣━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┫
┃                  │ 1234567 │             │             │            │             │ SUNGROW      │              ┃
┃                  │ 1234567 │             │             │            │             │ SUNGROW      │              ┃
┗━━━━━━━━━━━━━━━━━━┷━━━━━━━━━┷━━━━━━━━━━━━━┷━━━━━━━━━━━━━┷━━━━━━━━━━━━┷━━━━━━━━━━━━━┷━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━┛
```

#### Test Ps details API
```
./bin/darwin_arm64/GoSungrow api get getPsDetailWithPsType '{"ps_id":"1234567"}'
```

#### Set the Ps ID in the .env file
```
PS_ID=1234567
```

### Run the service
```
python3 main.py
```

#### Sample output
```
battery_level_percent=62.2 charging_discharging_power=-5.33 load_power=0.253 power_grid_power=-0.419 pv_power=6.002
```

