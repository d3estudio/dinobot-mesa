<template>
  <div class="uk-flex uk-flex-column uk-padding">
    <div class="uk-text-right">
      <router-link class="uk-link-reset" :to="{ name: 'logout' }">
        Sair <span data-uk-icon="icon: sign-out"/>
      </router-link>
    </div>
    <div class="uk-text-center">
      <img class="uk-width-1-3" src="/logo.png"/>
    </div>
    <div class="uk-flex uk-flex-none" data-uk-grid>
      <!-- TODO: Period is disabled because we added expenses API in the last minute -->
      <!-- <div class="uk-flex-first@s uk-width-1-1 uk-width-1-2@s">
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
      </div> -->
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
              <div class="uk-width-expand">
                Delivery
              </div>
              <small :class="color(netMarginByCategory('Delivery'))">
                {{ percentage(netMarginByCategory('Delivery')) }}
              </small>
            </div>
            <div class="uk-grid-small" data-uk-grid>
              <div class="uk-width-expand" data-uk-leader>
                Faturamento
              </div>
              <div>
                R$ {{ revenueByCategory('Delivery').toFixed(2) }}
              </div>
            </div>
            <div class="uk-grid-small" data-uk-grid>
              <div class="uk-width-expand" data-uk-leader>
                Custos
              </div>
              <div :class="color(costsByCategory('Delivery'))">
                R$ {{ costsByCategory('Delivery').toFixed(2) }}
              </div>
            </div>
            <div class="uk-grid-small uk-text-bold" data-uk-grid>
              <div class="uk-width-expand" data-uk-leader>
                Resultado
              </div>
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
              <div class="uk-width-expand">
                Buffet
              </div>
              <small :class="color(netMarginByCategory('Buffet'))">
                {{ percentage(netMarginByCategory('Buffet')) }}
              </small>
            </div>
            <div class="uk-grid-small" data-uk-grid>
              <div class="uk-width-expand" data-uk-leader>
                Faturamento
              </div>
              <div>
                R$ {{ revenueByCategory('Buffet').toFixed(2) }}
              </div>
            </div>
            <div class="uk-grid-small" data-uk-grid>
              <div class="uk-width-expand" data-uk-leader>
                Custos
              </div>
              <div :class="color(costsByCategory('Buffet'))">
                R$ {{ costsByCategory('Buffet').toFixed(2) }}
              </div>
            </div>
            <div class="uk-grid-small uk-text-bold" data-uk-grid>
              <div class="uk-width-expand" data-uk-leader>
                Resultado
              </div>
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
              <div class="uk-width-expand">
                Empresas
              </div>
              <small :class="color(netMarginByCategory('Empresas'))">
                {{ percentage(netMarginByCategory('Empresas')) }}
              </small>
            </div>
            <div class="uk-grid-small" data-uk-grid>
              <div class="uk-width-expand" data-uk-leader>
                Faturamento
              </div>
              <div>
                R$ {{ revenueByCategory('Empresas').toFixed(2) }}
              </div>
            </div>
            <div class="uk-grid-small" data-uk-grid>
              <div class="uk-width-expand" data-uk-leader>
                Custos
              </div>
              <div :class="color(costsByCategory('Empresas'))">
                R$ {{ costsByCategory('Empresas').toFixed(2) }}
              </div>
            </div>
            <div class="uk-grid-small uk-text-bold" data-uk-grid>
              <div class="uk-width-expand" data-uk-leader>
                Resultado
              </div>
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
      period: 30,
      percentages: {
        Buffet: 0.43,
        Empresas: 0.75,
        Delivery: 0.71,
      },
      expenses: {},
      items: [],
    };
  },
  methods: {
    async loadHandler() {
      const sales = await Client.post('ReportSale/ListReportSaleByTotal', {
        StartDate: DateTime.local().endOf('day').minus({ days: this.period }).toISO(),
        EndDate: DateTime.local().endOf('day').toISO(),
      });

      this.items = sales.data.Items;

      const expenses = await Client.post('FinancialCashFlow/Get', {
        DateFrom: DateTime.local().endOf('day').minus({ days: this.period }).toISO(),
        DateTo: DateTime.local().endOf('day').toISO(),
      });

      this.expenses = expenses.data.Item.DayRows.find(row => row.Name === 'Saídas');
    },
    itemsByCategory(category) {
      return this.items.filter(item => item.Category === category);
    },
    revenueTotal() {
      return this.items
        .reduce((total, item) => total + item.TotalPrice, 0);
    },
    revenueByCategory(category) {
      return this.itemsByCategory(category)
        .reduce((total, item) => total + item.TotalPrice, 0);
    },
    fixedCostsTotal() {
      // TODO: Remove this hardcoded -76000
      return this.revenueTotal() - this.expenses.Balance;
    },
    fixedCostsByCategory(category) {
      return this.fixedCostsTotal() * -(this.revenueByCategory(category) / this.revenueTotal());
    },
    variableCostsByCategory(category) {
      return -this.percentages[category] * this.revenueByCategory(category);
    },
    costsByCategory(category) {
      return this.variableCostsByCategory(category) + this.fixedCostsByCategory(category);
    },
    totalItemsByCategory(category) {
      return this.itemsByCategory(category)
        .reduce((total, item) => total + item.Quantity, 0);
    },
    resultByCategory(category) {
      return this.revenueByCategory(category) + this.costsByCategory(category);
    },
    percentage(value) {
      return `${Math.round(value * 100 || 0)}%`;
    },
    color(value) {
      return {
        'uk-text-danger': value < 0,
        'uk-text-success': value > 0,
      };
    },
    netMarginByCategory(category) {
      return 1 + (this.costsByCategory(category) / this.revenueByCategory(category));
    },
  },
  watch: {
    period: 'load',
  },
};
</script>
