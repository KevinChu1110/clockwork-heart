shader_type canvas_item;
render_mode blend_mix, unshaded;

/// 腳底軟影與接地硬影著色器：
/// 支援雙層接地陰影（大範圍漸層軟影 + 腳掌深色接觸硬影），消除角色浮空貼紙感。

uniform float strength : hint_range(0.0, 1.0) = 0.92;
uniform vec4 shadow_color : source_color = vec4(0.01, 0.01, 0.02, 1.0);
uniform float pixel_size : hint_range(1.0, 8.0) = 2.0;
uniform bool smooth_gradient = false;
uniform bool is_contact_shadow = false;

void fragment() {
	vec2 uv = UV;
	if (pixel_size > 1.0 && !smooth_gradient) {
		vec2 tex_size = vec2(textureSize(TEXTURE, 0));
		vec2 grid = tex_size / pixel_size;
		uv = (floor(UV * grid) + 0.5) / grid;
	}
	float raw_a = texture(TEXTURE, uv).a;
	float stepped_a = 0.0;

	if (is_contact_shadow) {
		// 深色接觸硬影：緊密高密度遮蔽核，邊緣扎實
		if (raw_a > 0.35) {
			stepped_a = 1.0;
		} else if (raw_a > 0.12) {
			stepped_a = 0.70;
		} else if (raw_a > 0.04) {
			stepped_a = 0.30;
		}
	} else if (smooth_gradient) {
		// 漸層軟影：平滑衰減，形成大氣漫射柔影
		stepped_a = smoothstep(0.01, 0.80, raw_a);
	} else {
		// 階梯式邊緣（相容既有基準）
		if (raw_a > 0.75) {
			stepped_a = 1.0;
		} else if (raw_a > 0.50) {
			stepped_a = 0.72;
		} else if (raw_a > 0.24) {
			stepped_a = 0.40;
		} else if (raw_a > 0.08) {
			stepped_a = 0.16;
		}
	}

	float a = stepped_a * COLOR.a * strength;
	COLOR = vec4(shadow_color.rgb, a);
}
