"""
checks if each item in a list of known bloatware is installed on your system,
and prompts for each installed whether you'd like to purge it. 
bloatware list from https://gist.github.com/NickSeagull/ed43a80db6a54d69ded3e18f8babaf19 
	, retrieved 08.05.20
"""

import subprocess

things = "account-plugin-aim account-plugin-facebook account-plugin-flickr account-plugin-jabber account-plugin-salut account-plugin-twitter account-plugin-windows-live account-plugin-yahoo aisleriot brltty colord deja-dup deja-dup-backend-gvfs duplicity empathy empathy-common evolution-data-server-online-accounts example-content firefox gnome-accessibility-themes gnome-contacts gnome-games-common gnome-mahjongg gnome-mines gnome-orca gnome-screensaver gnome-sudoku gnome-video-effects gnome-shell gnomine landscape-common libreoffice-avmedia-backend-gstreamer libreoffice-base-core libreoffice-calc libreoffice-common libreoffice-core libreoffice-draw libreoffice-gnome libreoffice-gtk libreoffice-impress libreoffice-math libreoffice-ogltrans libreoffice-pdfimport libreoffice-presentation-minimizer libreoffice-style-galaxy libreoffice-style-human libreoffice-writer libsane libsane-common mcp-account-manager-uoa python3-uno rhythmbox rhythmbox-plugins rhythmbox-plugin-zeitgeist sane-utils shotwell shotwell-common telepathy-gabble telepathy-haze telepathy-idle telepathy-indicator telepathy-logger telepathy-mission-control-5 telepathy-salut thunderbird thunderbird-gnome-support totem totem-common totem-plugins unity-lens-music unity-lens-photos unity-lens-video unity-webapps-common unity-scope-audacious unity-scope-chromiumbookmarks unity-scope-clementine unity-scope-colourlovers unity-scope-devhelp unity-scope-firefoxbookmarks unity-scope-gdrive unity-scope-gmusicbrowser unity-scope-gourmet unity-scope-guayadeque unity-scope-manpages unity-scope-musicstores unity-scope-musique unity-scope-openclipart unity-scope-texdoc unity-scope-tomboy unity-scope-video-remote unity-scope-virtualbox unity-scope-yelp unity-scope-zotero gbrainy landscape-client-ui-install printer-driver-brlaser printer-driver-foo2zjs printer-driver-foo2zjs-common printer-driver-m2300w printer-driver-ptouch printer-driver-splix unity-session unity ubuntu-session gdm3"

installed = set()
not_installed = set()

CMD_TEMPLATE = "dpkg -l | grep -E '^ii' | grep {thing}"

for i in things.split(' '):
	command = CMD_TEMPLATE.format(thing=i)

	output = subprocess.Popen( command , shell=True, stdout=subprocess.PIPE ).communicate()[0]
	#output = commands.getstatusoutput(command)
	(installed if len(output)>0 else not_installed).add(i)


print('\n# Installed: \n')
print('\t'+'\n\t'.join(sorted(installed)))

print('\n# Not installed: \n')
print('\t'+'\n\t'.join(sorted(not_installed)))

death_row = set()

for i in sorted(installed):
	if input("Purge {thing}? (y/n)".format(thing=i))=='y':
		death_row.add(i)
		print('  added to death row')
	else:
		print('  kay, keeping {thing}'.format(thing=i))


print('these will be deleted', death_row)
if input('rly delete all these? (y/n)')=='y':
	subprocess.Popen( 'sudo apt-get purge -y {thing}'.format(thing=' '.join(sorted(death_row))) , shell=True, stdout=subprocess.PIPE ).communicate()[0]

print('purging coplete. the following were spared: ')
print('\t'+'\n\t'.join([i for i in installed if i not in death_row]))

if len(death_row)>0:
    print('doing apt-get autoremove')
    subprocess.Popen( 'sudo apt-get autoremove -y ', shell=True, stdout=subprocess.PIPE ).communicate()[0]

print('installing XFCE4')	
subprocess.Popen( 'apt-get install xauth xorg lightdm lightdm-webkit-greeter xfce4 xfce4-goodies gnome-icon-theme -y', shell=True, stdout=subprocess.PIPE ).communicate()[0]
