import smta


'''
	sniffa il traffico fino a che non incontra una richista manifest
'''
manifest = smta.sniffa()
#print manifest

'''
	carica su redis le informazioni importanti del manifest
'''
smta.caricamanifest(manifest)

'''
	Cominicia a scaricare tutti i chunks al massimo bitrate e aggiorna redis
'''
smta.scarica(manifest)
