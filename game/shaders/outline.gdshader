shader_type canvas_item;

uniform vec4 outline_color : source_color = vec4(0.22, 0.14, 0.09, 1.0);
uniform float outline_width : hint_range(0.0, 10.0) = 2.0;

varying vec4 custom_modulate;

void vertex() {
	custom_modulate = COLOR;
}

void fragment() {
	vec4 col = texture(TEXTURE, UV);
	if (col.a > 0.35) {
		COLOR = col * custom_modulate;
	} else {
		vec2 size = TEXTURE_PIXEL_SIZE * outline_width;
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
			COLOR = vec4(outline_color.rgb, outline_color.a * max_a * custom_modulate.a);
		} else {
			COLOR = col * custom_modulate;
		}
	}
}
