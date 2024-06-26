import { Injectable } from '@nestjs/common';
import { AbilityFactory } from '@alvast-bedankt/gg-core';
import { {{cookiecutter.resource_singular}} } from './entities/{{cookiecutter.resource_kebap}}.entity.js';

@Injectable()
export class {{cookiecutter.resource_plural}}Abilities implements AbilityFactory {}
