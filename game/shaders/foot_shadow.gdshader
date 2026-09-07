shader_type canvas_item;
render_mode blend_mix, unshaded;

/// 腳底軟影：半透明深色橢圓蓋在地面（角色層下面，不蓋靴子）。
/// 不用乘色——草／深色石地乘完只是「更深的同色」，認不出橢圓。
uniform float strength : hint_range(0.0, 1.0) = 0.68;
uniform vec4 shadow_color : source_color = vec4(0.05, 0.04, 0.07, 1.0);

void fragment() {
	float a = texture(TEXTURE, UV).a * COLOR.a * strength;
	COLOR = vec4(shadow_color.rgb, a);
}
