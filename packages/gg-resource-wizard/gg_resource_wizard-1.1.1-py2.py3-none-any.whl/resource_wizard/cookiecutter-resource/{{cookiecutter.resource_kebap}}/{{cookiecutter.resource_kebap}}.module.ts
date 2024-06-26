import { {{cookiecutter.resource_plural}}Controller } from './{{cookiecutter.resource_kebap}}.controller.js';
import { {{cookiecutter.resource_plural}}Abilities } from './{{cookiecutter.resource_kebap}}.abilities.js';
import { ResourceModule } from '@alvast-bedankt/gg-core';

@ResourceModule({
    controllers: [{{cookiecutter.resource_plural}}Controller],
    abilities: [{{cookiecutter.resource_plural}}Abilities]
})
export class {{cookiecutter.resource_plural}}Module {}
