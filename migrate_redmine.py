#!/usr/bin/python

import paramiko

def setup_tygerteam_commands():
  raw_commands = '''
  rm -rf /tmp/redmine-files
  rm -rf /tmp/redmine-tables
  mkdir /tmp/redmine-files
  mkdir /tmp/redmine-tables
  '''
  commands = [i for i in raw_commands.split("\n")]
  return commands

def setup_chili_commands():
  raw_commands = '''
  vzctl enter 1003
  rm -rf /tmp/migration
  mkdir /tmp/migration
  chmod 777 /tmp/migration
  cd /tmp/migration
  su postgres
  pg_dump --no-owner -a -t attachments                        redmine > attachments.sql
  pg_dump --no-owner -a -t auth_sources                       redmine > auth_sources.sql
  pg_dump --no-owner -a -t boards                             redmine > boards.sql
  pg_dump --no-owner -a -t changes                            redmine > changes.sql
  pg_dump --no-owner -a -t changesets                         redmine > changesets.sql
  pg_dump --no-owner -a -t changesets_issues                  redmine > changesets_issues.sql
  pg_dump --no-owner -a -t comments                           redmine > comments.sql
  pg_dump --no-owner -a -t custom_fields                      redmine > custom_fields.sql
  pg_dump --no-owner -a -t custom_fields_projects             redmine > custom_fields_projects.sql
  pg_dump --no-owner -a -t custom_fields_trackers             redmine > custom_fields_trackers.sql
  pg_dump --no-owner -a -t custom_values                      redmine > custom_values.sql
  pg_dump --no-owner -a -t customers                          redmine > customers.sql
  pg_dump --no-owner -a -t deliverables                       redmine > deliverables.sql
  pg_dump --no-owner -a -t documents                          redmine > documents.sql
  pg_dump --no-owner -a -t enabled_modules                    redmine > enabled_modules.sql
  pg_dump --no-owner -a -t enumerations                       redmine > enumerations.sql
  pg_dump --no-owner -a -t groups_users                       redmine > groups_users.sql
  pg_dump --no-owner -a -t invoice_time_entries               redmine > invoice_time_entries.sql
  pg_dump --no-owner -a -t invoices                           redmine > invoices.sql
  pg_dump --no-owner -a -t issue_categories                   redmine > issue_categories.sql
  pg_dump --no-owner -a -t issue_relations                    redmine > issue_relations.sql
  pg_dump --no-owner -a -t issue_statuses                     redmine > issue_statuses.sql
  pg_dump --no-owner -a -t issues                             redmine > issues.sql
  pg_dump --no-owner -a -t journal_details                    redmine > journal_details.sql
  pg_dump --no-owner -a -t journals                           redmine > journals.sql
  pg_dump --no-owner -a -t kanban_issues                      redmine > kanban_issues.sql
  pg_dump --no-owner -a -t member_roles                       redmine > member_roles.sql
  pg_dump --no-owner -a -t members                            redmine > members.sql
  pg_dump --no-owner -a -t messages                           redmine > messages.sql
  pg_dump --no-owner -a -t news                               redmine > news.sql
  pg_dump --no-owner -a -t open_id_authentication_associations redmine > open_id_authentication_associations.sql
  pg_dump --no-owner -a -t open_id_authentication_nonces      redmine > open_id_authentication_nonces.sql
  pg_dump --no-owner -a -t payments                           redmine > payments.sql
  pg_dump --no-owner -a -t projects                           redmine > projects.sql
  pg_dump --no-owner -a -t projects_trackers                  redmine > projects_trackers.sql
  pg_dump --no-owner -a -t queries                            redmine > queries.sql
  pg_dump --no-owner -a -t rates                            redmine > rates.sql
  pg_dump --no-owner -a -t repositories                       redmine > repositories.sql
  pg_dump --no-owner -a -t roles                              redmine > roles.sql
  pg_dump --no-owner -a -t schema_migrations                  redmine > schema_migrations.sql
  pg_dump --no-owner -a -t settings                           redmine > settings.sql
  pg_dump --no-owner -a -t stuff_to_dos                       redmine > stuff_to_dos.sql
  pg_dump --no-owner -a -t taggins                            redmine > taggings.sql
  pg_dump --no-owner -a -t time_entries                       redmine > time_entries.sql
  pg_dump --no-owner -a -t time_grid_issues_users             redmine > time_grid_issues_users.sql
  pg_dump --no-owner -a -t timebanks                          redmine > timebanks.sql
  pg_dump --no-owner -a -t tokens                             redmine > tokens.sql
  pg_dump --no-owner -a -t trackers                           redmine > trackers.sql
  pg_dump --no-owner -a -t user_preferences                   redmine > user_preferences.sql
  pg_dump --no-owner -a -t users                              redmine > users.sql
  pg_dump --no-owner -a -t versions                           redmine > versions.sql
  pg_dump --no-owner -a -t watchers                           redmine > watchers.sql
  pg_dump --no-owner -a -t wiki_content_versions              redmine > wiki_content_versions.sql
  pg_dump --no-owner -a -t wiki_contents                      redmine > wiki_contents.sql
  pg_dump --no-owner -a -t wiki_pages                         redmine > wiki_pages.sql
  pg_dump --no-owner -a -t wiki_redirects                     redmine > wiki_redirects.sql
  pg_dump --no-owner -a -t wikis                              redmine > wikis.sql
  pg_dump --no-owner -a -t workflows              redmine > workflows.sql
  exit  # Exit the postgres account
  exit  # Exit the container
  scp /var/lib/vz/private/1003/tmp/*.sql root@www.tygerteam.com:/tmp/redmine-tables/
  scp /var/lib/vz/private/1003/var/www/rails_apps/chiliproject/files/* root@www.tygerteam.com:/tmp/redmine-files/
  '''
  commands = [i for i in raw_commands.split("\n")]
  return commands


def setup_redmine_commands():
  raw_commands = '''
  CTID=6016
  CTNAME=redmine
  vzctl create $CTID --hostname $CTNAME.xelerance.com --name $CTNAME --ostemplate ubunta-12.04-i386
  vzctl set $CTID --ipadd 192.168.88.60 --privvmpages unlimited --save
  vzctl start $CTID
  vzctl enter $CTID
  echo 'Acquire::http::Proxy "http://192.168.88.24:3142/apt-cacher/";' > /etc/apt/apt.conf.d/01proxy
  apt-get update
  apt-get upgrade
  apt-get install postgresql
  apt-get install --no-install-recommends git rubygems ruby1.9.1-dev ruby-rmagick rake make gcc openssl
  apt-get install ruby-fastercsv libapache2-mod-passenger imagemagick libxml2-dev libxslt-dev logrotate ssl-cert
  exit
  scp root@www.tygerteam.com:/tmp/redmine-tables/* /VEs/private/$CTID/tmp/migration/
  scp root@www.tygerteam.com:/tmp/redmine-files/* /VEs/private/$CTID/var/lib/redmine/default/files/
  vzctl enter $CTID
  REDMINE_PASSWORD=$(openssl rand -base64 33)
  cd /tmp/migration
  su postgres
  createuser redmine --no-superuser --no-createdb --no-createrole --login --encrypted
  psql << EOM
  alter user redmine PASSWORD '$REDMINE_PASSWORD';
  \q
  EOM
  createdb --owner=redmine --encoding=utf-8 -T template0 redmine
  for x in `ls *.sql` ; do psql redmine -c \"delete from ${x%.sql}\" ; done
  sed -ibk \"s/custom_filter/filter/\" auth_sources.sql
  sed -ibk \"s/created_at/created_on/\" issues.sql
  sed -ibk \"s/journaled_id/journalized_id/\" journals.sql
  sed -ibk \"s/lock_version/version/\" wiki_contents.sql
  for x in `ls *.sql` ; do psql redmine < $x 1>> /tmp/output.txt 2>&1; done
  exit  # Get out of Postgres user
  cd /var/www
  git clone https://github.com/redmine/redmine
  cd redmine
  git checkout 2.4-stable
  cd /var/www/redmine
  gem install bundler
  cd /var/www/redmine
  RAILS_ENV="production" bundle install --without development test mysql mysql2 sqlite sqlite3 sqlserver openid ldap 
  mkdir /var/www/redmine/plugins
  cd /var/www/redmine/plugins/
  git clone https://github.com/h0tw1r3/redmine-customer-plugin.git
  cat << EOF > /var/www/redmine/config/database.yml
  production:
    adapter: postgresql
    database: redmine
    host: 127.0.0.1
    username: redmine
    password: "$REDMINE_PASSWORD"
    encoding: utf8
  EOF
  unset REDMINE_PASSWORD
  chmod 640 /var/www/redmine/config/database.yml
  chgrp www-data /var/www/redmine/config/database.yml

  RAILS_ENV="production" bundle exec rake db:migrate
  RAILS_ENV="production" bundle exec rake db:migrate:plugins
  cat << EOF > /etc/logrotate.d/redmine
  /var/www/redmine/log/*.log {
  daily
  missingok
  rotate 7
  compress
  notifempty
  copytruncate
  }
  EOF
  cd /var/www/redmine
  mkdir -p tmp tmp/pdf public/plugin_assets
  chown -R www-data: files log tmp public/plugin_assets
  chmod -R 0755 files log tmp public/plugin_assets
  chmod -x log/*.log
  a2dismod authz_default authz_groupfile cgid env negotiation status > /dev/null
  cat << EOF > /etc/apache2/sites-available/redmine.xelerance.com.conf
  # Passenger tuning
  PassengerMaxPoolSize 2
  #PassengerMinInstance 1
  #PassengerSpawnMethod smart
  PassengerMaxRequests 1000
  PassengerUploadBufferDir /tmp/
  # Breaks compatibility with mod_autoindex and mod_rewrite
  PassengerHighPerformance on
  PassengerDefaultUser www-data
  #PassengerPreStart http://redmine.xelerance.com/

  <VirtualHost *:80>
      DocumentRoot /var/www/redmine/public
      ServerName redmine.xelerance.com
      CustomLog /var/www/redmine/log/access.log combined
      ErrorLog /var/www/redmine/log/error.log

      <Directory /var/www/redmine/public>
         AllowOverride None
         Options FollowSymLinks
         Order deny,allow
         Allow from all
      </Directory>
  </VirtualHost>
  EOF
  a2dissite default 000-default
  a2dissite default-ssl
  a2ensite redmine.xelerance.com
  a2enmod ssl
  apache2ctl -S && service apache2 restart
  '''
  commands = [i for i in raw_commands.split("\n")]
  return commands

def run_on(commands,host="localhost",port=22,username='root'):
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(
              paramiko.AutoAddPolicy())
  ssh.connect(host, port=port,username=username, allow_agent=True)
  
  session = ssh.invoke_shell()
  
  buff = ''
  while not buff.endswith('# '):
    resp = session.recv(9999)
    buff += resp
  
  for command in commands:
    session.send (command+"\n")
    buff = ''
    while not (buff.endswith('# ') or buff.endswith('$ ')):
      resp = session.recv(9999)
      buff += resp
    print buff
  
  ssh.close()

# MAIN

commands = setup_tygerteam_commands()
run_on(commands, 'www.tygerteam.com', port=22, username='root')

commands = setup_chili_commands()
run_on(commands, host='173.230.133.71', port=2022, username='root')

commands = setup_redmine_commands()
run_on(commands, '192.168.88.6', port=22, username='root')
