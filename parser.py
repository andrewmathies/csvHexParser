import csv
import numpy as np
import json

hexData = []
diagnostics = []

def eights(string):
	return [string[i:i+8] for i in range(0, len(string), 8)]

def buildObject(metadata, arr):
	uartD = {}
	
	uartD['validPacketsRecieved'] = arr[0]
	uartD['invalidLengthPacketsReceived'] = arr[1]
	uartD['invalidCrcPacketsReceived'] = arr[2]
	uartD['packetsInterruptedDuringReception'] = arr[3]
	uartD['bytesReceivedThatWereNotPartOfAPacket'] = arr[4]
	uartD['interByteTimeoutsDuringReception'] = arr[5]
	uartD['validPacketsSent'] = arr[6]
	uartD['retriesSent'] = arr[7]
	uartD['packetsNotAcked'] = arr[8]
	uartD['packetsNotSentBecauseRetriesExhausted'] = arr[9]
	uartD['packetsNotSentBecausePayloadWasTooLarge'] = arr[10]
	uartD['packetsNotSentBecauseQueueWasFull'] = arr[11]
	uartD['collisionsDetected'] = arr[12]
	uartD['serialErrors'] = arr[13]
	uartD['framingErrors'] = arr[14]
	uartD['bufferOverrunErrors'] = arr[15]

	entry = {}
	entry['Timestamp'] = metadata[0]
	entry['Direction'] = metadata[1]
	entry['Status'] = metadata[2]
	entry['Source'] = metadata[3]
	entry['Destination'] = metadata[4]
	entry['Command'] = metadata[5]
	entry['Length'] = metadata[6]
	entry['Crc'] = metadata[7]
	entry['Data'] = uartD

	diagnostics.append(entry)

with open('oven_on.csv') as offcsvfile:
	reader = csv.reader(offcsvfile, delimiter=',')

	for row in reader:
		if row[5] == '0xF0' and row[1] == 'Received':
			hexData.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))


for row in hexData:
	data = row[8]
	metadata = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])	

	f0response = data[10:138]
	f1response = data[144:272]
	f2response = data[278:]	

	responses = [f0response, f1response, f2response]

	#print f0Data + ' ' + str(len(f0Data))
	#print f1Data + ' ' + str(len(f1Data))
	#print f2Data + ' ' + str(len(f2Data))
	
	nums = []

	for response in responses:
		for val in eights(response):
			num = int(val, 16)
			nums.append(num)

		buildObject(metadata, nums)
		nums = []

#print('length of data', len(hexData))
print 'writing to data.json'

with open('oven_on.json', 'w') as outfile:
	json.dump(diagnostics, outfile, sort_keys=True)


