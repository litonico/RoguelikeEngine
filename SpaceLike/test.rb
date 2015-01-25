require 'minitest/autorun'
require './array'

describe Array3D do
  before do
    @array = Array3D.new 20, 20, 20
  end

  describe "when creating an array" do
    it "must have accessable dimensions" do
      @array.dim_x == 20
      @array.dim_y == 20
      @array.dim_z == 20
    end
  end

  describe "when getting a property" do
    it "must be brace-accessable" do
      @array[1, 1, 1]
    end
  end

  describe "when settinga property" do
    it "must be brace-accessable" do
      # @array[1][1][1] = 5
      @array[1, 1, 1] = 5
    end
  end

  describe "when setting everything at once" do
    it "must set every single value" do
      @array.set_uniform! "#"

      (0...@array.dim_x).each do |x|
        (0...@array.dim_y).each do |y|
          (0...@array.dim_z).each do |z|
            @array[x, y, z].must_equal("#")
          end
        end
      end

    end
  end

end
