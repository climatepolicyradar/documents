/**
 * doc controller
 */

import { factories } from "@strapi/strapi";

export default factories.createCoreController("api::doc.doc", ({ strapi }) => ({
  async updateByImportId(ctx) {
    const { import_id } = ctx.params;

    const docs = await strapi.db.query("api::doc.doc").findMany({
      where: {
        identifiers: {
          identifier: {
            $eq: import_id,
          },
        },
        publishedAt: {
          $notNull: true,
        },
      },
      populate: ["*"],
    });

    ctx.body = docs;
  },
}));
