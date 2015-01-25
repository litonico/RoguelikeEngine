require './array'

class Coords
  attr_accessor :x, :y, :z

  def initialize x, y, z
    @x = x
    @y = y
    @z = z
  end
end

# materials = [
#   "empty",
#   "rock"
# ]

DIFFUSION_SPEED = 0.01

class Tile
  def initialize background_gas, concentration, material

    # Is the tile filled with a material?
    @material = material

    if material != "empty"
      background_gas = {}
    else
      # Gas amounts (since tiles are constant-sized, density can be derived)
      @background_gas = { background_gas => concentration }
    end
  end

  def diffuse_into neighbor
    this_total_gas = self.background_gas.values.fold(:+)
    neighbor_total_gas = neighbor.background_gas.values.fold(:+)
    difference = this_total_gas - neighbor_total_gas

    amount = difference/2 * DIFFUSION_SPEED
    for gas in self.background_gas.keys
      self.background_gas[gas] -= amount
      neighbor[gas] += amount
    end
  end

  attr_accessor :background_gas, :material
end

class Entity
  attr_accessor :inventory, :health, :air, :pos

  def initialize x, y, z
    @inventory = []
    @health = 100
    @air = 100
    @pos = Coords.new x, y, z
  end

end

class Hero < Entity
end

class World
  attr_accessor :map

  def initialize dim_x, dim_y, dim_z
    @map = Array3D.new dim_x, dim_y, dim_z
    @map.set_uniform! Tile.new "air", 100, "empty"
  end

  def diffuse
    # TODO: This is a guess at a less slow way to do this.
    # Move through the array in steps of two, diffusing in to the
    # 26 surrounding cells, so each cell only takes its 
    # neighbor's contributions.

    (0...@map.dim_x).step(2) do |x|
      (0...@map.dim_y).step(2) do |y|
        (0...@map.dim_z).step(2) do |z|
          # Back
          if x != 0
            @map[x, y, z].diffuse_into @map[x-1, y, z]
            @map[x, y, z].diffuse_into @map[x-1, y, z+1]
            @map[x, y, z].diffuse_into @map[x-1, y+1, z]
            @map[x, y, z].diffuse_into @map[x-1, y+1, z+1]
          end

          # Front
          if x != dim_x
            @map[x, y, z].diffuse_into @map[x+1, y, z]
            @map[x, y, z].diffuse_into @map[x+1, y, z+1]
            @map[x, y, z].diffuse_into @map[x+1, y+1, z]
            @map[x, y, z].diffuse_into @map[x+1, y+1, z+1]
          end
          
          # Top
          if y != dim_y
            @map[x, y, z].diffuse_into @map[x, y-1, z]
            @map[x, y, z].diffuse_into @map[x, y-1, z+1]
            @map[x, y, z].diffuse_into @map[x+1, y-1, z]
            @map[x, y, z].diffuse_into @map[x+1, y-1, z+1]
          end

          # Bottom
          if y != dim_y
            @map[x, y, z].diffuse_into @map[x, y+1, z]
            @map[x, y, z].diffuse_into @map[x, y+1, z+1]
            @map[x, y, z].diffuse_into @map[x+1, y+1, z]
            @map[x, y, z].diffuse_into @map[x+1, y+1, z+1]
          end

          # Left
          if y != dim_y
            @map[x, y, z].diffuse_into @map[x, y, z-1]
            @map[x, y, z].diffuse_into @map[x, y-1, z-1]
            @map[x, y, z].diffuse_into @map[x+1, y, z-1]
            @map[x, y, z].diffuse_into @map[x+1, y-1, z-1]
          end

          # Right
          if y != dim_y
            @map[x, y, z].diffuse_into @map[x, y, z+1]
            @map[x, y, z].diffuse_into @map[x, y-1, z+1]
            @map[x, y, z].diffuse_into @map[x+1, y, z+1]
            @map[x, y, z].diffuse_into @map[x+1, y-1, z+1]
          end

        end
      end
    end
  end
end

class Game
  attr_accessor :hero, :entities, :world, :hero, :current_entity
  # @actors = []
  def initialize
    @entities = []
    @world = World.new 10, 10, 10
    @hero = Entity.new 0, 0, 0
    @current_entity = 0
  end

  def step
    @world.diffuse
    # @entities[@current_entity].update
    # @current_entity = (@current_entity+1) % @entities.length
  end
end

class ASCII_ui
  attr_accessor :game

  def initialize
    @game = Game.new
  end

  def render!
    # Draw the current level, as well as ones on z-levels above and below it.
    current_z = @game.hero.pos.z

    map = @game.world.map
    (0...map.dim_x).each do |x|
      (0...map.dim_y).each do |y|
        # Check if entities on that level
        print self.draw_background map[x, y, current_z]
      end
      print "\n"
    end
  end

  def step
    @game.step
  end

  def draw_background tile
    if tile.background_gas["air"] > 30
      return '#'
    else
      return '.'
    end
  end
end

def main
  ui = ASCII_ui.new
  ui.render!
  ui.step
end

main
