<mujoco model="elderly_assist_robot">
  <compiler angle="radian" inertiafromgeom="true"/>

  <!-- 世界体：地面 + 障碍物（模拟小区桌椅、台阶） -->
  <worldbody>
    <!-- 地面：摩擦系数0.8（模拟瓷砖/水泥地） -->
    <geom name="floor" type="plane" size="10 10 0.1" rgba="0.2 0.2 0.2 1" friction="0.8 0.1 0.1"/>

    <!-- 障碍物1：桌子（x=3,y=0，宽1m、高0.7m） -->
    <geom name="table" type="box" pos="3 0 0.35" size="0.5 0.5 0.7" rgba="0.8 0.4 0.4 1" friction="0.6 0.1 0.1"/>
    <!-- 障碍物2：椅子（x=-3,y=2，宽0.4m、高0.9m） -->
    <geom name="chair" type="box" pos="-3 2 0.45" size="0.2 0.2 0.9" rgba="0.4 0.8 0.4 1" friction="0.6 0.1 0.1"/>
    <!-- 障碍物3：门槛（x=0,y=5，宽0.2m、高0.1m） -->
    <geom name="threshold" type="box" pos="0 5 0.05" size="2 0.1 0.1" rgba="0.6 0.6 0.6 1" friction="0.9 0.1 0.1"/>

    <!-- 机器人本体：底盘 + 四个轮子 + 货箱 -->
    <body name="chassis" pos="0 0 0.2">
      <!-- 底盘：长方体，长1m、宽0.6m、高0.2m -->
      <geom name="chassis_geom" type="box" size="0.5 0.3 0.2" rgba="0.1 0.1 0.8 1" mass="5" 
            friction="0.8 0.1 0.1" damping="0.1 0.1 0"/>

      <!-- 前左轮：半径0.1m，距底盘中心(0.25, 0.2) -->
      <body name="wheel_fl" pos="0.25 0.2 0.1">
        <geom name="wheel_fl_geom" type="cylinder" size="0.1 0.05" rgba="0.3 0.3 0.3 1" mass="1" 
              friction="0.9 0.1 0.1" damping="0.1 0.1 0"/>
        <joint name="joint_fl" type="hinge" axis="0 1 0" pos="0 0 0" range="-1e6 1e6" damping="0.1"/>
      </body>

      <!-- 前右轮：半径0.1m -->
      <body name="wheel_fr" pos="0.25 -0.2 0.1">
        <geom name="wheel_fr_geom" type="cylinder" size="0.1 0.05" rgba="0.3 0.3 0.3 1" mass="1" 
              friction="0.9 0.1 0.1" damping="0.1 0.1 0"/>
        <joint name="joint_fr" type="hinge" axis="0 1 0" pos="0 0 0" range="-1e6 1e6" damping="0.1"/>
      </body>

      <!-- 后左轮 -->
      <body name="wheel_rl" pos="-0.25 0.2 0.1">
        <geom name="wheel_rl_geom" type="cylinder" size="0.1 0.05" rgba="0.3 0.3 0.3 1" mass="1" 
              friction="0.9 0.1 0.1" damping="0.1 0.1 0"/>
        <joint name="joint_rl" type="hinge" axis="0 1 0" pos="0 0 0" range="-1e6 1e6" damping="0.1"/>
      </body>

      <!-- 后右轮 -->
      <body name="wheel_rr" pos="-0.25 -0.2 0.1">
        <geom name="wheel_rr_geom" type="cylinder" size="0.1 0.05" rgba="0.3 0.3 0.3 1" mass="1" 
              friction="0.9 0.1 0.1" damping="0.1 0.1 0"/>
        <joint name="joint_rr" type="hinge" axis="0 1 0" pos="0 0 0" range="-1e6 1e6" damping="0.1"/>
      </body>

      <!-- 货箱：在底盘上方 -->
      <body name="cargo" pos="0 0 0.3">
        <geom name="cargo_geom" type="box" size="0.4 0.2 0.2" rgba="0.8 0.8 0.1 1" mass="2" 
              friction="0.5 0.1 0.1" damping="0.2 0.2 0"/>
      </body>
    </body>
  </worldbody>

  <!-- 执行器：控制四个轮子的电机（力矩控制） -->
  <actuator>
    <motor name="motor_fl" joint="joint_fl" gear="100" ctrlrange="-10 10"/>
    <motor name="motor_fr" joint="joint_fr" gear="100" ctrlrange="-10 10"/>
    <motor name="motor_rl" joint="joint_rl" gear="100" ctrlrange="-10 10"/>
    <motor name="motor_rr" joint="joint_rr" gear="100" ctrlrange="-10 10"/>
  </actuator>

  <!-- 默认状态 -->
  <default>
    <joint damping="0.1" armature="0.1"/>
    <geom friction="0.8 0.1 0.1" density="1000"/>
  </default>
</mujoco>