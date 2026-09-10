shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture, filter_linear;
uniform float saturation : hint_range(0.0, 3.0) = 1.08;
uniform float contrast : hint_range(0.0, 3.0) = 1.08;
uniform float brightness : hint_range(0.0, 3.0) = 1.03;

void fragment() {
	vec4 col = texture(screen_texture, SCREEN_UV);
	vec3 rgb = (col.rgb - vec3(0.5)) * contrast + vec3(0.5);
	rgb *= brightness;
	float luma = dot(rgb, vec3(0.2126, 0.7152, 0.0722));
	// Highlight protection: preserve metallic reflections and prevent blowout into warm tones
	float sat = mix(saturation, 1.0, smoothstep(0.70, 0.98, luma));
	rgb = mix(vec3(luma), rgb, sat);
	COLOR = vec4(clamp(rgb, 0.0, 1.0), 1.0);
}
