import type { Schema, Struct } from '@strapi/strapi';

export interface IdentifiersIdentifiers extends Struct.ComponentSchema {
  collectionName: 'components_identifiers_identifiers';
  info: {
    description: '';
    displayName: 'Identifiers';
  };
  attributes: {
    identifier: Schema.Attribute.String & Schema.Attribute.Required;
    source: Schema.Attribute.Enumeration<['navigator-admin']>;
  };
}

declare module '@strapi/strapi' {
  export module Public {
    export interface ComponentSchemas {
      'identifiers.identifiers': IdentifiersIdentifiers;
    }
  }
}
