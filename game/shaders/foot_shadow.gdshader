shader_type canvas_item;
render_mode blend_mix, unshaded;

/// 腳底軟影：接近不透明的深色核＋階梯式像素化邊緣（降低平滑向量羽化感，契合點陣像素美術）。
uniform float strength : hint_range(0.0, 1.0) = 0.92;
uniform vec4 shadow_color : source_color = vec4(0.01, 0.01, 0.02, 1.0);
uniform float pixel_size : hint_range(1.0, 8.0) = 2.0;

void fragment() {
	vec2 uv = UV;
	if (pixel_size > 1.0) {
		vec2 tex_size = vec2(textureSize(TEXTURE, 0));
		vec2 grid = tex_size / pixel_size;
		uv = (floor(UV * grid) + 0.5) / grid;
	}
	float raw_a = texture(TEXTURE, uv).a;
	// 階梯式邊緣：量化為像素階梯，降低平滑高斯感
	float stepped_a = 0.0;
	if (raw_a > 0.75) {
		stepped_a = 1.0;
	} else if (raw_a > 0.50) {
		stepped_a = 0.72;
	} else if (raw_a > 0.24) {
		stepped_a = 0.40;
	} else if (raw_a > 0.08) {
		stepped_a = 0.16;
	}
	float a = stepped_a * COLOR.a * strength;
	COLOR = vec4(shadow_color.rgb, a);
}
