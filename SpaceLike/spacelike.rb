require './array'

class Coords
  # Wrapper around coordinates (for entities and items) so they can be 
  # accessed with dot-operations.
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

DIFFUSION_SPEED = 0.5

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
    unless neighbor.material == "empty"
      this_total_gas = self.background_gas.values.reduce(:+)
      neighbor_total_gas = neighbor.background_gas.values.reduce(:+)
      difference = this_total_gas - neighbor_total_gas

      amount = (difference/2) * DIFFUSION_SPEED

      for gas in @background_gas.keys
        # `amount` is the total amount of gas moving from one tile to the 
        # other, so we distribute that amount among all the tile's gases.
        # In the case that either of the `total_gas`es is 0, no gas flows
        # *from* that tile. This also saves us from div/0 errors!
        if this_total_gas != 0
          @background_gas[gas] -= (amount/this_total_gas)*@background_gas[gas]
        end
        if neighbor_total_gas != 0
          neighbor.background_gas[gas] += (amount/neighbor_total_gas) \
                                          *neighbor.background_gas[gas]
        end
      end
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
  attr_accessor :view_dist
  def initialize x, y, z
    super(x, y, z)
    @view_dist = 10
  end
end

class World
  attr_accessor :map

  def initialize dim_x, dim_y, dim_z
    @map = Array3D.new dim_x, dim_y, dim_z
    @map.set_uniform! do
      Tile.new "air", 10, "empty"
    end
  end

  def diffuse
    # TODO: This just is a guess at a less dumb way to do this.
    # Move through the array in steps of two, diffusing in to the
    # 26 surrounding cells, so each cell only takes its 
    # neighbor's contributions.
    dim_x, dim_y, dim_z = @map.dim_x, @map.dim_y, @map.dim_z

    (0...dim_x).step(2) do |g_x|
      (0...dim_y).step(2) do |g_y|
        (0...dim_z).step(2) do |g_z|

          xs = [g_x-1, g_x, g_x+1].select {|i| i >= 0 && i < dim_x}
          ys = [g_y-1, g_y, g_y+1].select {|i| i >= 0 && i < dim_y}
          zs = [g_z-1, g_z, g_z+1].select {|i| i >= 0 && i < dim_z}

          xs.each do |x|
            ys.each do |y|
              zs.each do |z|
                # TODO: Each tile first tries to diffuse into itself.
                # This isn't a problem really, but could be fixed.
                @map[g_x, g_y, g_z].diffuse_into @map[x, y, z]
              end
            end
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
    @current_entity = 0
    @hero = Hero.new 3, 4, 0
    @world = World.new 5, 7, 1
    @world.map[0,0,0] = Tile.new "air", 100, "empty"
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

  def color text, color
    colors = {
      'black' => "\033[0m" ,
      'grey'  => "\033[90m",
      'red'   => "\033[91m",
      'green' => "\033[92m",
      'yellow'=> "\033[93m",
      'blue'  => "\033[94m",
      'purple'=> "\033[95m",
      'cyan'  => "\033[96m",
      'white' => "\033[97m",
      }

    #TODO: It's more complicated than this...
    neutral = colors['black']

    colors[color] + text + neutral
  end
  
  def clear
    print "\x1b[2J\x1b[H"
  end

  def render!
    # Draw the current level, as well as ones on z-levels above and below it.
    z = @game.hero.pos.z
    self.render_slice! z

    # TODO: To draw the level above and below the player
    # zs = [z-1, z, z+1].select {|i| i >= 0 && i < @game.world.map.dim_x}
    # zs.each do |level|
    #   self.render_slice! level
    #   puts "\n"
    #   puts level
    # end

    gets
    self.clear
  end

  def render_slice! current_z
    #TODO: Base this on view distance, not map size
    map = @game.world.map
    hero = @game.hero

    x_view_range = (hero.pos.x-hero.view_dist...hero.pos.x+hero.view_dist)
    y_view_range = (hero.pos.y-hero.view_dist...hero.pos.y+hero.view_dist)

    x_view_range.each do |x|
      unless x < 0 || x >= map.dim_x
        y_view_range.each do |y|
          unless y < 0 || y >= map.dim_y
            # TODO: Check if entities on that level
            print self.draw_background map[x, y, current_z]
          end
        end
        print "\n"
      end
    end
  end

  def step
    @game.step
  end

  def draw_background tile
    if tile.background_gas["air"] > 60
      return color('#', 'blue')
    elsif tile.background_gas["air"] > 12
      return color('#', 'cyan')
    else
      return color('.', 'grey')
    end
  end
end

def main
  ui = ASCII_ui.new
  (1..25).each do 
    ui.render!
    ui.step
  end
end

main
