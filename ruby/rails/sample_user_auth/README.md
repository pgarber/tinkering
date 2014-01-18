Goal is to support:
 - User is able to login/logout
 - Database is MongoDB
 - RSpec is used for testing

##
Below are notes on how to achieve above:
##

Create new rails app defaulting to rspec for tests
Nice article: http://www.rubyinside.com/how-to-rails-3-and-rspec-2-4336.html
1.  rails new MYAPP -T --skip-active-record
    The -T option tells rails not to include Test::Unit
    --skip-active-record skip ActiveRecord since we plan to use mongoid 
2.  edit 'Gemfile'
     gem ‘rspec-rails’
3.  bundle install
4.  rails g rspec:install

Configure mongoid so we can use MongoDB
http://mongoid.org/en/mongoid/docs/installation.html
1. edit 'Gemfile'
    gem "mongoid", ">= 3.1.2"
2. bundle install
3. rails g mongoid:config
4. edit 'config/mongoid.yml' if desired, can use defaults for now


** Update rspec to use database_cleaner so test DB is wiped out after each spec runs
** Add FactoryGirl


Configure devise
1. edit 'Gemfile'
     gem 'devise'
2. rails generate devise:install
3. Recommended from devise install 
  edit app/views/application.html.erb
    Added:
      <p class="notice"><%= notice %></p>
      <p class="alert"><%= alert %></p>
  edit routes.rb
    Ensure a 'root_url' is defined
    root :to => "home#index"
 4. rails g devise:views
     Copies the devise default views into our app so we can edit them

Create User model for Devise to use
# http://railsapps.github.io/tutorial-rails-mongoid-devise.html
1. rails generate devise User
2. edit 'config/application.rb'
   Disable logging of the password fields
	config.filter_parameters += [:password, :password_confirmation]

Create a Home Page
1. rm public/index.html
2. rails generate controller home index
3. Update the home page to display the users so we can see if things are working
   a) edit app/controllers/home_controller.rb
    class HomeController < ApplicationController
      def index
        @users = User.all
      end
    end

   b) edit app/views/home/index.html.erb
     <h3>Home</h3>
     <% @users.each do |user| %>
       <p>User: <%= user.email %> </p>
     <% end %>
4. Create some sample users
     edit db/seeds.rb
		puts 'SETTING UP DEFAULT USER LOGIN'
		user = User.create! :email => 'user@example.com', :password => 'password', :password_confirmation => 'password'
		puts 'New user created: ' << user.name
		user2 = User.create! :email => 'user2@example.com', :password => 'password', :password_confirmation => 'password'
		puts 'New user created: ' << user2.name
	5. rake db:mongoid:create_indexes
	6. rake db:seed
	* If we want to delete DB we can run:
	   rake db:drop