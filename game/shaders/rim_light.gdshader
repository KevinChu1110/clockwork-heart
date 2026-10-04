shader_type canvas_item;
render_mode blend_mix;

/// 楓之谷 × 塔塔冒險 2.2 頭身角色：深暖褐外描邊 ＋ 金色天宮 Rim Light 邊緣輪廓光著色器
/// 消除貼紙感，吃背景以太晨曦光源反射，增加立體受光層次。

uniform vec4 outline_color : source_color = vec4(0.22, 0.14, 0.09, 1.0);
uniform float outline_width : hint_range(0.0, 8.0) = 2.6;
uniform bool outline_enabled = true;

uniform bool rim_enabled = true;
uniform vec4 rim_color : source_color = vec4(1.0, 0.82, 0.20, 1.0); // 鮮亮金色晨曦反光
uniform float rim_width : hint_range(0.5, 16.0) = 6.0;
uniform float rim_intensity : hint_range(0.0, 3.0) = 1.8;
uniform vec2 rim_direction = vec2(0.15, -0.95);

varying vec4 custom_modulate;

void vertex() {
	custom_modulate = COLOR;
}

void fragment() {
	vec4 col = texture(TEXTURE, UV);
	vec2 ps = TEXTURE_PIXEL_SIZE;

	if (col.a > 0.35) {
		vec3 base_rgb = col.rgb;
		if (rim_enabled && rim_intensity > 0.001) {
			vec2 dir = normalize(rim_direction);
			vec2 perp = vec2(-dir.y, dir.x);

			// 迎光面邊界採樣（朝向光源方向外側）
			float a_sun = texture(TEXTURE, UV + dir * ps * rim_width).a;
			float a_sun_left = texture(TEXTURE, UV + (dir * 0.85 + perp * 0.52) * ps * rim_width).a;
			float a_sun_right = texture(TEXTURE, UV + (dir * 0.85 - perp * 0.52) * ps * rim_width).a;
			float sun_edge = clamp(1.0 - (a_sun * 0.50 + (a_sun_left + a_sun_right) * 0.25), 0.0, 1.0);

			// 全向邊緣微光採樣（消除整圈死板貼紙感）
			float a_down = texture(TEXTURE, UV - dir * ps * (rim_width * 0.65)).a;
			float a_left = texture(TEXTURE, UV + perp * ps * (rim_width * 0.65)).a;
			float a_right = texture(TEXTURE, UV - perp * ps * (rim_width * 0.65)).a;
			float all_edge = clamp(1.0 - min(min(a_sun, a_down), min(a_left, a_right)), 0.0, 1.0);

			// 迎光金色強調光 (75%) + 全身立體通透輪廓微光 (25%)
			float rim_factor = clamp(sun_edge * 0.80 + all_edge * 0.20, 0.0, 1.0);
			rim_factor = pow(rim_factor, 0.90);

			// 染色混合 (Tint) + 加色泛光：即使在純白毛髮/衣物上也能鮮明呈現金色邊緣輪廓光！
			float blend_amt = clamp(rim_factor * rim_intensity * 0.85, 0.0, 0.95);
			vec3 tinted = mix(base_rgb, rim_color.rgb, blend_amt);
			base_rgb = tinted + rim_color.rgb * (rim_factor * rim_intensity * 0.50);
		}
		COLOR = vec4(base_rgb, col.a) * custom_modulate;
	} else if (outline_enabled && outline_width > 0.01) {
		// 外描邊
		vec2 size = ps * outline_width;
		float max_a = 0.0;
		max_a = max(max_a, texture(TEXTURE, UV + vec2(size.x, 0.0)).a);
		max_a = max(max_a, texture(TEXTURE, UV - vec2(size.x, 0.0)).a);
		max_a = max(max_a, texture(TEXTURE, UV + vec2(0.0, size.y)).a);
		max_a = max(max_a, texture(TEXTURE, UV - vec2(0.0, size.y)).a);
		max_a = max(max_a, texture(TEXTURE, UV + vec2(size.x, size.y) * 0.7071).a);
		max_a = max(max_a, texture(TEXTURE, UV + vec2(-size.x, size.y) * 0.7071).a);
		max_a = max(max_a, texture(TEXTURE, UV + vec2(size.x, -size.y) * 0.7071).a);
		max_a = max(max_a, texture(TEXTURE, UV + vec2(-size.x, -size.y) * 0.7071).a);

		if (max_a > 0.35) {
			// 雙色動態受光描邊：迎光輪廓融合璀璨金色以太光輝，背光面維持深暖褐
			vec2 dir = normalize(rim_direction);
			float a_body_below = texture(TEXTURE, UV - dir * ps * (outline_width + 2.5)).a;
			float rim_glow_factor = clamp(a_body_below * 1.6, 0.0, 1.0);
			vec4 edge_col = mix(outline_color, vec4(rim_color.rgb * 1.15, 1.0), rim_glow_factor * 0.80);
			COLOR = vec4(edge_col.rgb, edge_col.a * max_a * custom_modulate.a);
		} else {
			COLOR = col * custom_modulate;
		}
	} else {
		COLOR = col * custom_modulate;
	}
}
