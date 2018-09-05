/**
 * Created by Vinícius Fragoso Pinheiro <vfragosop@gmail.com>
 */

export default {
  data() {
    return {
      loading: false,
      loadingError: null,
    };
  },
  created() {
    this.load();
  },
  methods: {
    async load() {
      this.loading = true;
      this.loadingError = null;

      try {
        const response = await this.loadHandler();
        this.loadSuccess(response);
      } catch (reason) {
        this.loadingError = reason;
        this.loadError(reason);
      } finally {
        this.loading = false;
      }
    },
    loadHandler() {},
    loadError() {},
    loadSuccess() {},
  },
};
