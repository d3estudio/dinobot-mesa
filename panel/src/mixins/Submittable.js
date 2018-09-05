/**
 * Created by Vinícius Fragoso Pinheiro <vfragosop@gmail.com>
 */

export default {
  data() {
    return {
      failed: false,
      submitting: false,
      errors: {},
    };
  },
  methods: {
    async submit() {
      this.failed = false;
      this.submitting = true;

      try {
        const response = await this.submitHandler();
        this.submitSuccess(response);
      } catch (reason) {
        if (reason.validationErrors) {
          this.errors = reason.validationErrors;
        } else {
          this.failed = true;
        }
        this.submitError(reason);
      } finally {
        this.submitting = false;
      }
    },
    submitHandler() {},
    submitError() {},
    submitSuccess() {},
  },
};
