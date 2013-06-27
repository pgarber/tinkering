class CreateGenresMovies < ActiveRecord::Migration
  def up
    create_table :genres_movies, :id => false do |t|
      t.belongs_to :movie
      t.belongs_to :genre
    end
  end

  def down
    drop_table :genres_movies
  end
end
