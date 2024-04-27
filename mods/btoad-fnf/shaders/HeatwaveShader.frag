//SHADERTOY PORT FIX
#pragma header
vec2 uv = openfl_TextureCoordv.xy;
vec2 fragCoord = openfl_TextureCoordv*openfl_TextureSize;
vec2 iResolution = openfl_TextureSize;
uniform float iTime;
#define iChannel0 bitmap
#define texture flixel_texture2D
#define fragColor gl_FragColor
#define mainImage main

#define STRENGTH 0.11
#define RAD 0.9
#define SPEED 9.9

void mainImage()
{
    // Normalized pixel coordinates (from 0 to 1)
    vec2 uv = fragCoord/iResolution.xy;

    // Time varying pixel color
    float jacked_time = 5.5*iTime;
    const vec2 scale = vec2(.1);
   	
    uv += 0.01*sin(scale*jacked_time + length( uv )*10.0);
    fragColor = texture(iChannel0, uv).rgba;
}