shader_type canvas_item;
render_mode blend_mix, unshaded;

/// 腳底軟影：接近不透明的深色核＋柔邊橢圓，蓋在地面（角色層下面，不蓋靴子）。
/// 深色石地要原圖縮小時一眼看得出踩在地上；0.68 核在荒路石板上會融化。
uniform float strength : hint_range(0.0, 1.0) = 0.92;
uniform vec4 shadow_color : source_color = vec4(0.01, 0.01, 0.02, 1.0);

void fragment() {
	float a = texture(TEXTURE, UV).a * COLOR.a * strength;
	COLOR = vec4(shadow_color.rgb, a);
}
