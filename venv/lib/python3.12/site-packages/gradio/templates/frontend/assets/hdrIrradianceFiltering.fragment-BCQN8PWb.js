import{j as e}from"./index-Bjh7sNQ4.js";import"./helperFunctions-CtH_JZFf.js";import"./hdrFilteringFunctions-Dn4zeP_c.js";import"./index-Dx60bCjY.js";import"./svelte/svelte.js";const r="hdrIrradianceFilteringPixelShader",i=`#include<helperFunctions>
#include<importanceSampling>
#include<pbrBRDFFunctions>
#include<hdrFilteringFunctions>
uniform samplerCube inputTexture;
#ifdef IBL_CDF_FILTERING
uniform sampler2D icdfTexture;
#endif
uniform vec2 vFilteringInfo;uniform float hdrScale;varying vec3 direction;void main() {vec3 color=irradiance(inputTexture,direction,vFilteringInfo
#ifdef IBL_CDF_FILTERING
,icdfTexture
#endif
);gl_FragColor=vec4(color*hdrScale,1.0);}`;e.ShadersStore[r]||(e.ShadersStore[r]=i);const a={name:r,shader:i};export{a as hdrIrradianceFilteringPixelShader};
//# sourceMappingURL=hdrIrradianceFiltering.fragment-BCQN8PWb.js.map
