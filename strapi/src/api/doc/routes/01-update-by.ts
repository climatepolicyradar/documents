export default {
  routes: [
    {
      method: "GET",
      path: "/docs/import_id/:import_id",
      handler: "doc.updateByImportId",
      config: {
        auth: false,
      },
    },
  ],
};
