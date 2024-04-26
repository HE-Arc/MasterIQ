# config valid for current version and patch releases of Capistrano
lock "~> 3.18.1"

set :application, "masteriq"
set :repo_url, "https://github.com/HE-Arc/MasterIQ.git"
# append :linked_files, '.env'
# Default branch is :master
# ask :branch, `git rev-parse --abbrev-ref HEAD`.chomp

# Default deploy_to directory is /var/www/my_app_name
# set :deploy_to, "/var/www/my_app_name"

# Default value for :format is :airbrussh.
# set :format, :airbrussh

# You can configure the Airbrussh format using :format_options.
# These are the defaults.
# set :format_options, command_output: true, log_file: "log/capistrano.log", color: :auto, truncate: :auto

# Default value for :pty is false
# set :pty, true

# Default value for :linked_files is []
# append :linked_files, "config/database.yml", 'config/master.key'

# Default value for linked_dirs is []
# append :linked_dirs, "log", "tmp/pids", "tmp/cache", "tmp/sockets", "public/system", "vendor", "storage"

# Default value for default_env is {}
# set :default_env, { path: "/opt/ruby/bin:$PATH" }

# Default value for local_user is ENV['USER']
# set :local_user, -> { `git config user.name`.chomp }

# Default value for keep_releases is 5
# set :keep_releases, 5

# Uncomment the following to require manually verifying the host key before first deploy.
# set :ssh_options, verify_host_key: :secure

after 'deploy:updating', 'env:copy'
namespace :env do
  desc "Copy env files"
  task :copy do
    on roles([:app, :web]) do |h|
      execute "ln -nfs #{shared_path}/.env.api #{release_path}/api/.env"
      execute "ln -nfs #{shared_path}/.env.front #{release_path}/frontend/.env"
    end
  end
end

after 'deploy:updating', 'pip:install'

namespace :pip do
  desc 'Pip install'
  task :install do
    on roles([:app, :web]) do |h|
      execute "pip install -r #{release_path}/api/requirements.txt"
    end
  end
end

after 'deploy:updating', 'django:collectstatic'

namespace :django do
  desc 'Install static files'
  task :collectstatic do
    on roles([:app, :web]) do |h|
     within "#{release_path}/api" do
        execute :python3, 'manage.py', 'collectstatic'
      end 
    end
  end
end

after 'deploy:updating', 'npm:install'
namespace :npm do
  desc 'NPM install'
  task :install do
    on roles([:app, :web]) do |h|
        execute "npm install --prefix #{release_path}/frontend"
    end
  end
end

after 'deploy:updating', 'npm:build'
namespace :npm do
  desc 'NPM install'
  task :build do
    on roles([:app, :web]) do |h|
        execute "npm run build --prefix #{release_path}/frontend"
    end
  end
end

after 'deploy:updating', 'django:migrate'
namespace :django do
  desc 'Django migrations'
  task :migrate do
    on roles([:app, :web]) do |h|
      within "#{release_path}/api" do
        execute :python3, 'manage.py', 'migrate'
      end
    end
  end
end

after 'deploy:publishing', 'nginx:restart'

namespace :nginx do
  desc 'Restart application'
  task :restart do
    on roles(:web) do |h|
      execute :sudo, 'service nginx restart'
    end
  end
end

after 'deploy:publishing', 'gunicorn:restart'

namespace :gunicorn do
  desc 'Restart application'
  task :restart do
    on roles(:web) do |h|
      within "#{release_path}" do
        execute :sudo, './restart-gunicorn.sh'
      end
    end
  end
end

