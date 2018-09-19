<template>
  <div class="uk-flex uk-flex-column uk-padding">
    <div class="uk-text-right">
      Olá Xandão,
      <router-link class="uk-link-reset uk-text-bold" :to="{ name: 'logout' }">
        Sair <span data-uk-icon="icon: sign-out"/>
      </router-link>
    </div>
    <div class="uk-text-center">
      <img class="uk-width-1-3" src="/logo.png"/>
    </div>
    <div class="uk-flex uk-flex-none" data-uk-grid>
      <!-- TODO: Period is disabled because we added expenses API in the last minute -->
      <div class="uk-flex-first@s uk-width-1-1 uk-width-1-2@s">
        <ul class="uk-subnav uk-subnav-pill">
          <li :class="{ 'uk-active': period === 1 }">
            <a @click.prevent="period = 1">Hoje</a>
          </li>
          <li :class="{ 'uk-active': period === 7 }">
            <a @click.prevent="period = 7">7 Dias</a>
          </li>
          <li :class="{ 'uk-active': period === 30 }">
            <a @click.prevent="period = 30">30 Dias</a>
          </li>
        </ul>
      </div>
    </div>
    <div v-if="loading" class="uk-flex-auto uk-flex uk-flex-center uk-flex-middle">
      <div data-uk-spinner/>
    </div>
    <div v-else class="uk-flex-auto" data-uk-grid>
      <div class="uk-width-1-3@s uk-width-1-1">
        <div class="uk-card uk-card-default">
          <div class="uk-card-media-top">
            <img src="/cards/capa_dash_delivery.png" alt="">
          </div>
          <div class="uk-card-body">
            <div class="uk-card-title uk-grid-small uk-margin uk-flex-bottom" data-uk-grid>
              <div class="uk-width-expand">Delivery</div>
              <small class="uk-text-muted">{{ percentage(contributionByCategory('Delivery')) }}</small>
            </div>
            <div class="uk-grid-small" data-uk-grid>
              <div class="uk-width-expand" data-uk-leader>Faturamento</div>
              <div>
                R$ {{ revenueByCategory('Delivery').toFixed(2) }}
              </div>
            </div>
            <div class="uk-grid-small" data-uk-grid>
              <div class="uk-width-expand" data-uk-leader>Custos</div>
              <div :class="color(expensesByCategory('Delivery'))">
                R$ {{ expensesByCategory('Delivery').toFixed(2) }}
              </div>
            </div>
            <div class="uk-grid-small" data-uk-grid>
              <div class="uk-width-expand" data-uk-leader>Margem</div>
              <div :class="color(resultByCategory('Delivery'))">
                {{ percentage(netMarginByCategory('Delivery')) }}
              </div>
            </div>
            <div class="uk-grid-small uk-text-bold" data-uk-grid>
              <div class="uk-width-expand" data-uk-leader>Resultado</div>
              <div :class="color(resultByCategory('Delivery'))">
                R$ {{ resultByCategory('Delivery').toFixed(2) }}
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="uk-width-1-3@s uk-width-1-1">
        <div class="uk-card uk-card-default">
          <div class="uk-card-media-top">
            <img src="/cards/capa_dash_buffet.png" alt="">
          </div>
          <div class="uk-card-body">
            <div class="uk-card-title uk-grid-small uk-margin uk-flex-bottom" data-uk-grid>
              <div class="uk-width-expand">Buffet</div>
              <small class="uk-text-muted">{{ percentage(contributionByCategory('Buffet')) }}</small>
            </div>
            <div class="uk-grid-small" data-uk-grid>
              <div class="uk-width-expand" data-uk-leader>Faturamento</div>
              <div>
                R$ {{ revenueByCategory('Buffet').toFixed(2) }}
              </div>
            </div>
            <div class="uk-grid-small" data-uk-grid>
              <div class="uk-width-expand" data-uk-leader>Custos</div>
              <div :class="color(expensesByCategory('Buffet'))">
                R$ {{ expensesByCategory('Buffet').toFixed(2) }}
              </div>
            </div>
            <div class="uk-grid-small" data-uk-grid>
              <div class="uk-width-expand" data-uk-leader>Margem</div>
              <div :class="color(resultByCategory('Buffet'))">
                {{ percentage(netMarginByCategory('Buffet')) }}
              </div>
            </div>
            <div class="uk-grid-small uk-text-bold" data-uk-grid>
              <div class="uk-width-expand" data-uk-leader>Resultado</div>
              <div :class="color(resultByCategory('Buffet'))">
                R$ {{ resultByCategory('Buffet').toFixed(2) }}
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="uk-width-1-3@s uk-width-1-1">
        <div class="uk-card uk-card-default">
          <div class="uk-card-media-top">
            <img src="/cards/capa_dash_empresas.png" alt="">
          </div>
          <div class="uk-card-body">
            <div class="uk-card-title uk-grid-small uk-margin uk-flex-bottom" data-uk-grid>
              <div class="uk-width-expand">Empresas</div>
              <small class="uk-text-muted">{{ percentage(contributionByCategory('Empresas')) }}</small>
            </div>
            <div class="uk-grid-small" data-uk-grid>
              <div class="uk-width-expand" data-uk-leader>Faturamento</div>
              <div>
                R$ {{ revenueByCategory('Empresas').toFixed(2) }}
              </div>
            </div>
            <div class="uk-grid-small" data-uk-grid>
              <div class="uk-width-expand" data-uk-leader>Custos</div>
              <div :class="color(expensesByCategory('Empresas'))">
                R$ {{ expensesByCategory('Empresas').toFixed(2) }}
              </div>
            </div>
            <div class="uk-grid-small" data-uk-grid>
              <div class="uk-width-expand" data-uk-leader>Margem</div>
              <div :class="color(resultByCategory('Empresas'))">
                {{ percentage(netMarginByCategory('Empresas')) }}
              </div>
            </div>
            <div class="uk-grid-small uk-text-bold" data-uk-grid>
              <div class="uk-width-expand" data-uk-leader>Resultado</div>
              <div :class="color(resultByCategory('Empresas'))">
                R$ {{ resultByCategory('Empresas').toFixed(2) }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { DateTime } from 'luxon';
import Client from '../api';
import Loadable from '../mixins/Loadable';

export default {
  mixins: [
    Loadable,
  ],
  data() {
    return {
      period: 1,
      financialFlow: [],
      sales: [],
    };
  },
  computed: {
    totalRevenue() {
      return this.revenueByCategory('Delivery')
        + this.revenueByCategory('Buffet')
        + this.revenueByCategory('Empresas');
    },
    totalExpenses() {
      return this.financialFlow.DayRows
        .find(row => row.Name === 'Saídas')
        .Balance;
    },
  },
  methods: {
    async loadHandler() {
      await this.loadSales();
      await this.loadExpenses();
    },
    async loadSales() {
      const response = await Client.post('ReportSale/ListReportSaleByTotal', {
        StartDate: DateTime.local().endOf('day').minus({ days: this.period }).toISO(),
        EndDate: DateTime.local().endOf('day').toISO(),
      });

      this.sales = response.data.Items;
    },
    async loadExpenses() {
      const response = await Client.post('FinancialCashFlow/Get', {
        DateFrom: DateTime.local().endOf('day').minus({ days: this.period }).toISO(),
        DateTo: DateTime.local().endOf('day').toISO(),
      });

      this.financialFlow = response.data.Item;
    },
    /**
     * By Category
     */
    salesByCategory(category) {
      return this.sales.filter(item => item.Category === category);
    },
    revenueByCategory(category) {
      return this.salesByCategory(category)
        .reduce((total, item) => total + item.TotalPrice, 0);
    },
    contributionByCategory(category) {
      return (this.revenueByCategory(category) / this.totalRevenue);
    },
    expensesByCategory(category) {
      return this.totalExpenses * this.contributionByCategory(category);
    },
    resultByCategory(category) {
      return this.revenueByCategory(category) + this.expensesByCategory(category);
    },
    netMarginByCategory(category) {
      return 1 + (this.expensesByCategory(category) / this.revenueByCategory(category));
    },
    /**
     * Utils
     */
    percentage(value) {
      return `${Math.round(value * 100 || 0)}%`;
    },
    color(value) {
      return {
        'uk-text-danger': value < 0,
        'uk-text-success': value > 0,
      };
    },
  },
  watch: {
    period: 'load',
  },
};
</script>
