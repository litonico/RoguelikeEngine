class Array3D
  attr_accessor :contents
  attr_reader :dim_x, :dim_y, :dim_z

  def initialize dim_x, dim_y, dim_z
    @dim_x = dim_x
    @dim_y = dim_y
    @dim_z = dim_z
    @contents = Array.new (dim_x) {
                  Array.new(dim_y) {
                    Array.new(dim_z)
                  }
                }
  end

  def[] x, y, z
    @contents[x][y][z]
  end

  def[]= x, y, z, val
    @contents[x][y][z] = val
  end

  def set_uniform! &val
    (0...@dim_x).each do |x|
      (0...@dim_y).each do |y|
        (0...@dim_z).each do |z|
          @contents[x][y][z] = val.call
        end
      end
    end
  end

end


