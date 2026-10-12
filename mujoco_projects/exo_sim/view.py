import mujoco
import mujoco.viewer

model = mujoco.MjModel.from_xml_path("elbow.xml")
data = mujoco.MjData(model)

mujoco.viewer.launch(model, data)
