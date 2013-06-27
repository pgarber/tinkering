Given /^a genre named Comedy$/ do
  @comedy = Genre.create!(:name => "Comedy")
end

When /^I create a movie Caddyshack in the Comedy genre$/ do
  visit movies_path
  click_link "Add Movie"
  #save_and_open_page
  fill_in "Title", :with => "Caddyshack"
  select "1980", :from => "Release year"
  check "Comedy"
  click_button  "Save"
end

Then /^Caddyshack should be in the Comedy genre$/ do
  visit genres_path
  click_link "Comedy"
  print "response is <#{response}>"
  page.should have_content("1 movie")
  page.should have_content("Caddyshack")
end

